import pandas as pd
import os
import json

def save_json(data, base_filename, output_dir="data"):
    """
    Save a list of dictionaries to JSON format.

    Parameters:
    - data: list of dicts
    - base_filename: base name without extension (e.g., "pdb_entries")
    - output_dir: directory to save the files (default = "data/")
    """
    os.makedirs(output_dir, exist_ok=True)

    # Save JSON
    json_path = os.path.join(output_dir, f"{base_filename}.json")
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved JSON to {json_path}")