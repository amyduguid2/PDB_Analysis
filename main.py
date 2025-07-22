#import necessary libraries
from datetime import datetime
import pandas as pd

#import custom functions
from src.fetch_pdb import fetch_pdb
from src.fetch_articles import parse_pdb
from src.fetch_articles import fetch_epmc
from src.utils import save_json
from src.parse_results import extract_epmc_metadata
from src.parse_results import extract_epmc_authors
from src.parse_results import enrich_epmc_with_pdb_ids

### Data Retrieval ###
#This section fetches PDB entries released in the last 5 years
#and saves them in both CSV and JSON formats. 
# It also parses the fetched data to extract metadata and PubMed IDs,
#and fetches Europe PMC article metadata for the PubMed IDs.     
# The results are saved in the specified output directory.           

#Get the current year and calculate the start year
#This will be used to fetch PDB entries from the last 5 years
today = datetime.today()
today_year = today.year
five_years_ago = today.year - 5

# Step 1: Fetch the PDB data
#pdb_data = fetch_pdb(start_year=five_years_ago, end_year=today_year, log_file="data/log_files/fetch_pdb_log.txt")

# Step 2: Save to both formats
#save_json(pdb_data, base_filename="pdb_entries", output_dir="data/data_retrieval")

# Step 3: Parse the fetched data to extract metadata and PubMed IDs
# This will also save the cleaned metadata and PubMed IDs to separate files
#pubmed_ids = parse_pdb(input_json_path="data/data_retrieval/pdb_entries.json",
#                  output_csv_path="data/data_retrieval/parsed_pdb_entries.csv",
#                  pubmed_ids_path="data/data_retrieval/pubmed_ids.txt")

# Step 4: Fetch PMC Article Metadata for PDB PMIDs
#epmc_metadata = fetch_epmc(pubmed_ids, batch_size=1000, log_file="data/log_files/fetch_epmc_log.txt")

# Step 5: Save the EPMC metadata
#save_json(epmc_metadata, base_filename="epmc_metadata", output_dir="data/data_retrieval")

# Step 6: Extract and save the relevant EPMC metadata to a CSV file
metadata = extract_epmc_metadata(input_json_path="data/data_retrieval/epmc_metadata.json",
                       output_csv_path="data/data_retrieval/epmc_metadata.csv")

# Step 7: Extract authors and ORCID IDs from EPMC metadata
extract_epmc_authors(input_json_path="data/data_retrieval/epmc_metadata.json",
                     output_csv_path="data/data_retrieval/epmc_authors.csv")

# Step 8: Map PDB IDs to EPMC metadata
# This will create a mapping of PDB IDs to their corresponding EPMC metadata
enrich_epmc_with_pdb_ids(pdb_df=pd.read_csv("data/data_retrieval/parsed_pdb_entries.csv"),
                         epmc_df=metadata,
                         output_csv_path="data/data_retrieval/metadata_with_pdb.csv")
