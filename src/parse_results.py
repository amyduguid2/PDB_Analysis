import json
import pandas as pd
import ast
from collections import defaultdict
import pandas as pd

def extract_epmc_metadata(input_json_path, output_csv_path):
    """
    Extracts relevant metadata fields from Europe PMC raw JSON response and saves to a CSV.
    Parameters:
    - input_json_path: str, path to the saved raw Europe PMC JSON
    - output_csv_path: str, path to save cleaned metadata as CSV
    """
    # Load the JSON file
    with open(input_json_path, "r") as f:
        records = json.load(f)

    # Extract only relevant metadata fields
    cleaned = []
    for record in records:

        journal_info = record.get("journalInfo", {})
        journal = journal_info.get("journal", {})

        journal_title = journal.get("title")
        journal_nlmid = journal.get("nlmid")

        cleaned.append({
            "pmid": record.get("id"),
            "title": record.get("title"),
            "authors": record.get("authorString"),
            "affiliation": record.get("affiliation"),
            "journal": journal_title,
            "journal_nlmid": journal_nlmid,
            "year": record.get("pubYear"),
            "open_access": record.get("isOpenAccess"),
            "doi": record.get("doi"),
            "abstract": record.get("abstractText"),
            "Cited_by": record.get("citedByCount")
        })

    # Convert to DataFrame
    df = pd.DataFrame(cleaned)

    # Save to CSV
    df.to_csv(output_csv_path, index=False)
    print(f"Extracted metadata for {len(df)} articles.")
    print(f"Saved to: {output_csv_path}")
    return df

def extract_epmc_authors(input_json_path, output_csv_path):
    """
    Extracts authors and ORCID IDs for each article from Europe PMC JSON.
    Outputs long-format table with pmid, title, author name, and ORCID.
    """
    with open(input_json_path, "r") as f:
        records = json.load(f)

    author_rows = []

    for rec in records:
        pmid = rec.get("id")
        title = rec.get("title", "")
        authors = rec.get("authorList", {}).get("author", [])

        for author in authors:
            full_name = author.get("fullName")
            orcid = None

            if "authorId" in author and author["authorId"].get("type") == "ORCID":
                orcid = author["authorId"].get("value")

            author_rows.append({
                "pmid": pmid,
                "title": title,
                "author_fullName": full_name,
                "author_orcid": orcid
            })

    df = pd.DataFrame(author_rows)
    df.to_csv(output_csv_path, index=False)
    print(f"Saved author data for {len(df)} authors to {output_csv_path}")
    return df


def enrich_epmc_with_pdb_ids(pdb_df, epmc_df, output_csv_path):
    """
    Cleans and merges PDB metadata with EPMC metadata by mapping PubMed IDs to PDB IDs.

    Parameters:
        pdb_df (pd.DataFrame): DataFrame containing PDB metadata with 'fields.PUBMED'.
        epmc_df (pd.DataFrame): DataFrame containing EPMC metadata with 'pmid'.

    Returns:
        pd.DataFrame: EPMC DataFrame enriched with a 'pdb_ids' column listing matched PDB IDs.
    """

    # Step 1: Clean 'fields.PUBMED' in pdb_df
    pdb_df['fields.PUBMED'] = pdb_df['fields.PUBMED'].apply(
        lambda x: ast.literal_eval(x)[0] if isinstance(x, str) and x.startswith('[') else x
    )

    # Step 2: Ensure EPMC 'pmid' is string and stripped
    epmc_df["pmid"] = epmc_df["pmid"].astype(str).str.strip()

    # Step 3: Build PubMed → PDB ID mapping
    pubmed_to_pdb = defaultdict(list)
    for _, row in pdb_df.iterrows():
        pdb_id = row.get("id")
        pubmed_ids = row.get("fields.PUBMED", [])
        if isinstance(pubmed_ids, str):
            pubmed_ids = [pubmed_ids]
        for pmid in pubmed_ids:
            pubmed_to_pdb[pmid].append(pdb_id)

    # Step 4: Map PDB IDs into EPMC metadata
    epmc_df["pdb_ids"] = epmc_df["pmid"].map(pubmed_to_pdb)
    epmc_df.to_csv(output_csv_path, index=False)
    print(f"Saved enriched EPMC data with PDB IDs to {output_csv_path}")
