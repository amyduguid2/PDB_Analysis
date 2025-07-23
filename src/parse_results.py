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
