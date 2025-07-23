# Import necessary libraries
import pandas as pd
import requests
import json

def parse_pdb(input_json_path, output_csv_path, pubmed_ids_path):
    """
    Parses a raw JSON file of PDB entries to extract metadata and PubMed IDs.
    
    Parameters:
    - input_json_path: str, path to the saved raw JSON from PDB API
    - output_csv_path: str, path to save cleaned metadata
    - pubmed_ids_path: str, path to save list of PubMed IDs (one per line)
    """
    # Load JSON
    with open(input_json_path, "r") as f:
        data = json.load(f)

    # Expecting the JSON to be a list of entry dicts
    if isinstance(data, dict) and "entries" in data:
        entries = data["entries"]
    elif isinstance(data, list):
        entries = data
    else:
        raise ValueError("Unexpected JSON format. Expected list or dict with 'entries' key.")

    # Normalize to flat table
    df = pd.json_normalize(entries)

    # Save full metadata
    df.to_csv(output_csv_path, index=False)

    # Extract PubMed IDs
    pubmed_ids_raw = df.get("fields.PUBMED", [])

    # Clean and flatten
    clean_pubmed_ids = []
    for pmid in pubmed_ids_raw:
        if isinstance(pmid, list):
            clean_pubmed_ids.extend(pmid)
        elif isinstance(pmid, str):
            clean_pubmed_ids.append(pmid)

    # Remove duplicates
    clean_pubmed_ids = list(set(clean_pubmed_ids))

    # Save
    with open(pubmed_ids_path, "w") as f:
        f.write("\n".join(clean_pubmed_ids))

    print(f"{len(df)} PDB entries parsed containing {len(clean_pubmed_ids)} unique PubMed IDs.")
    print(f"PubMed IDs saved to: {pubmed_ids_path}")

    return clean_pubmed_ids

def fetch_epmc(pubmed_ids, batch_size=1000, log_file="data/fetch_epmc_log.txt"):
    """
    Fetch metadata from Europe PMC for a list of PubMed IDs.

    Parameters:
    - pubmed_ids: list of PubMed ID strings
    - batch_size: maximum number of PMIDs per POST (default 1000)
    - log_file: file to log progress and errors

    Returns:
    - results: list of metadata dictionaries
    """
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/searchPOST"
    headers = {"Accept": "application/json"}
    results = []

    with open(log_file, "w") as log:
        log.write(f"Starting Europe PMC metadata retrieval for {len(pubmed_ids)} PubMed IDs\n")
        print(f"Starting Europe PMC metadata retrieval for {len(pubmed_ids)} PubMed IDs")

        for i in range(0, len(pubmed_ids), batch_size):
            batch = pubmed_ids[i:i+batch_size]
            query = " OR ".join([f"EXT_ID:{pmid}" for pmid in batch])
            data = {
                "query": query,
                "format": "json",
                "resultType": "core",
                "pageSize": batch_size
            }

            retries = 0
            success = False

            while retries < 3 and not success:
                try:
                    response = requests.post(url, data=data, headers=headers, timeout=15)

                    if response.status_code == 200:
                        data = response.json()
                        entries = data.get("resultList", {}).get("result", [])
                        results.extend(entries)
                        log.write(f"Fetched {len(entries)} articles for batch {i} to {i+len(batch)}\n")
                        print(f"Fetched {len(entries)} articles for batch {i} to {i+len(batch)}")
                        success = True

                    else:
                        log.write(f"Error {response.status_code} on batch {i}-{i+len(batch)}: {response.text}\n")
                        print(f"Error {response.status_code} on batch {i}-{i+len(batch)}")
                        break  # Don't retry on 4xx/5xx if it's a bad query

                except requests.exceptions.RequestException as e:
                    retries += 1
                    log.write(f"Retry {retries}/3 failed on batch {i}-{i+len(batch)}: {e}\n")
                    print(f"Retry {retries}/3 failed on batch {i}-{i+len(batch)}: {e}")
                    time.sleep(5)

            if not success:
                log.write(f"Failed to fetch data for batch {i}-{i+len(batch)} after 3 retries\n")
                print(f"Failed to fetch data for batch {i}-{i+len(batch)} after 3 retries")

    print(f"Retrieved {len(results)} total articles from Europe PMC.")
    return results
