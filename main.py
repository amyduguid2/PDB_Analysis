#import necessary libraries
import time
import requests #used for making HTTP requests to the PDB API
import pandas as pd
import os
import json

#import custom functions
from src.fetch_pdb import fetch_pdb_entries
from src.utils import save_data

# Step 1: Fetch the PDB data
pdb_data = fetch_pdb_entries(start_year=2019, end_year=2024)

# Step 2: Save to both formats
save_data(pdb_data, base_filename="pdb_entries")

