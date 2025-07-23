#import necessary libraries
from datetime import datetime
import pandas as pd
import os

#import custom functions
from src.fetch_pdb import fetch_pdb
from src.fetch_articles import parse_pdb
from src.fetch_articles import fetch_epmc
from src.utils import save_json
from src.parse_results import extract_epmc_metadata
from src.parse_results import extract_epmc_authors

### Data Retrieval ###

"""
This script fetches PDB entries released in the last 5 years
and saves them in both CSV and JSON formats. 
It also parses the fetched PDB data to extract metadata and PubMed IDs,
and fetches Europe PMC article metadata for the PubMed IDs.
The script then extracts relevant metadata from the Europe PMC articles,
and extracts authors and ORCID IDs.
Finally, it maps PDB IDs to Europe PMC metadata.        
The results are saved in the specified output directory.  
    """

#Ensure directories exist
#make directory for output if it doesn't exist
data_dir = "data"
os.makedirs(data_dir, exist_ok=True)
log_dir = "data/log_files"
os.makedirs(log_dir, exist_ok=True)


#Get the current year and calculate the start year
#This will be used to fetch PDB entries from the last 5 years
today = datetime.today()
today_year = today.year
five_years_ago = today.year - 5

# Step 1: Fetch the PDB data
pdb_data = fetch_pdb(start_year=five_years_ago, end_year=today_year, log_file="data/log_files/fetch_pdb_log.txt")

# Step 2: Save to both formats
save_json(pdb_data, base_filename="pdb_entries", output_dir="data")

# Step 3: Parse the fetched data to extract metadata and PubMed IDs
# This will also save the cleaned metadata and PubMed IDs to separate files
pubmed_ids = parse_pdb(input_json_path="data/pdb_entries.json",
                       output_csv_path="data/parsed_pdb_entries.csv",
                       pubmed_ids_path="data/pubmed_ids.txt")

# Step 4: Fetch PMC Article Metadata for PDB PMIDs
epmc_metadata = fetch_epmc(pubmed_ids, batch_size=1000, log_file="data/log_files/fetch_epmc_log.txt")

# Step 5: Save the EPMC metadata
save_json(epmc_metadata, base_filename="epmc_metadata", output_dir="data")

# Step 6: Extract and save the relevant EPMC metadata to a CSV file
metadata = extract_epmc_metadata(input_json_path="data/epmc_metadata.json",
                                 output_csv_path="data/epmc_metadata.csv")

# Step 7: Extract authors and ORCID IDs from EPMC metadata
extract_epmc_authors(input_json_path="data/epmc_metadata.json",
                     output_csv_path="data/epmc_authors.csv")