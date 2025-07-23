#import required libraries
import time
import requests #used for making HTTP requests to the PDB API

### Function to fetch PDB entries released between start and end years ###
def fetch_pdb(start_year, end_year, log_file="data/log_files/fetch_pdb_log.txt"):
    # Specify the URL for the PDB API endpoint
    url = "https://www.ebi.ac.uk/ebisearch/ws/rest/pdbe"
    # Specify that we want the response in JSON format
    headers = {"Accept": "application/json"}
    # Create empty list to store the results
    results = [] 

    # Open the log file to write the fetched entries
    with open(log_file, "w") as log:
        for year in range(start_year, end_year + 1):
            print(f"Fetching entries for year: {year}")
            log.write(f"Fetching entries for year: {year}\n")
            start = 0  # Starting index for pagination
            size = 100
            filter = f'creation_date:["{year}/01/01" TO "{year}/12/31"]'  # Number of entries to fetch per request
            # Loop to fetch all entries for the current year in batches

            hit_count = None

            while True:
                # Stop paginating if we already know start is past the end
                if hit_count is not None and start >= hit_count:
                    break
                
                params = {
                    "query": "*:*",   # Fetch all entries           
                    "start": start,   # Starting index
                    "size": size,     # Fetch 1000 entries per request
                    "format": "json", # Specifying the format of the response
                    "fields": "id,description,PUBMED,acc,domain_source,name,creation_date",  # Fields to include in the response
                    "filter": filter  # Filter to fetch entries created in the specified year
                }
                
                retries = 0
                success = False

                while retries < 3 and not success:

                    # Handling the response
                    try:
                        # Making the GET request to the PDB API
                        response = requests.get(url, params=params, headers=headers, timeout=10)

                        if response.status_code == 200:  # Check if the request was successful
                            data = response.json()  # Parse the JSON response

                            # Find total number of entries for the year
                            if hit_count is None:
                                hit_count = int(data.get("hitCount", 0))
                                print(f"Total entries for {year}: {hit_count}")
                                log.write(f"Total entries for {year}: {hit_count}\n")

                            # Extract the entries from the response
                            entries = data.get('entries', [])
                            if not entries:  # If no entries are returned, break the loop
                                break
                            results.extend(entries)  # Add the fetched entries to the results list
                            log.write(f"Fetched {len(entries)} entries for year {year}, start index {start}.\n")
                            print(f"Fetched {len(entries)} entries for year {year}, start index {start}.")
                            success = True
                        
                        # Handle unexpected response formats
                        else:
                            log.write(f"Error {response.status_code} for year {year}, start {start}: {response.text}\n")
                            print(f"Error {response.status_code} for year {year}, start {start}: {response.text}")
                            break

                    # Handle any exceptions that may occur during the request
                    except requests.exceptions.RequestException as e:
                        retries += 1
                        log.write(f"Retry {retries}/3 failed for year {year}, start {start}: {e}\n")
                        log.write("Retrying in 5 seconds...\n")
                        print(f"Retry {retries}/3 failed for year {year}, start {start}: {e}")
                        print("Retrying in 5 seconds...")
                        time.sleep(5)  # Wait 5 seconds and retry the request
                        continue  # Retry the loop

                if not success:
                    log.write(f"Failed to fetch data for year {year}, start {start} after 3 retries.\n")
                    print(f"Failed to fetch data for year {year}, start {start} after 3 retries.")
                    break  # Skip to next year if repeated failures

                # Increment the starting index for the next batch of entries
                start += size

    return results