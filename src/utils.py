import pandas as pd
import os
import json

def save_data(data, base_filename, output_dir="data"):
    """
    Save a list of dictionaries to both JSON and CSV formats.

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

    # Save CSV
    csv_path = os.path.join(output_dir, f"{base_filename}.csv")
    try:
        df = pd.DataFrame(data)
        df.to_csv(csv_path, index=False)
        print(f"Saved CSV to {csv_path}")
    except ValueError as e:
        print(f"Could not save CSV: {e}")