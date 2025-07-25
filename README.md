# PDB Publication Mapping – EMBL-EBI Data Science Task
_Amy Duguid_

## Project Overview
This project retrieves and analyses Protein Data Bank (PDB) entries from the past five years, mapping them to their associated publications via the Europe PMC API. 
It identifies publishing trends, top contributors, and collaboration networks, and includes both visual and statistical summaries in the final report.

To access the final report, click [here.](Report.md)

---

## File Structure
```text
📁 PDB_Analysis/
├── 📄 README.md
├── 📄 Report.md                 # Summary Report (Findings, Visualisation, Challenges)
├── 📄 main.py                   # Entry point to run full pipeline
├── 📁 data/
│   └── .gitignore to ignore large output files from main.py
├── 📁 src/                      # Preprocessing and utility scripts
│   ├── fetch_pdb.py             # API calls, raw data PDB data retrieval
│   ├── fetch_articles.py        # API calls, raw data EPMC data retrieval
│   ├── parse_results.py         # Parsing, cleaning, mapping
│   └── utils.py                 # Data Saving Function
├── 📁 notebooks/
│   └── analysis.ipynb           # Visualisations, Charts, Commentary
├── 📁 output/                  # Output folder from analysis.ipynb
│   ├── top_10_authors.csv        
│   ├── top_10_affiliations.csv   
│   ├── top_10_journals.csv       
│   ├── top_10_collaborations.csv       
│   └── figures/
│       ├── publication_distribution_lineplot.png
│       ├── pdbe_article_growth.png
│       ├── pdb_entries_growth.png
│       ├── orcid_coverage_pie_chart.png 
│       └── author_collab_network.html     
├── 📄 .gitignore                # Ignore data folder
└── 📄 requirements.txt          # All packages used (pyvis, pandas etc.)
```

---

## Setup Instructions:

### 1. Clone Github Repository
```bash
git clone https://github.com/amyduguid2/PDB_Analysis.git
cd PDB_Analysis
```

### 2. Create Environment
Option 1: Conda (Recommended)
```bash
conda env create -f environment.yml
conda activate pdb-analysis
```
Option 2: Pip
```bash
pip install -r requirements.txt
```

---

### 3. Run main.py
This script will retrieve PDB entries from the last 5 years using EBI API.
Following this, the script uses Europe PMC API to extract associated metadata.

Output files:
- data/pdb_entries.json = pdb API call raw data
- data/parsed_pdb_entries.csv = cleaned PDB metadata
- data/epmc_metadata.json = epmc API call raw data
- data/epmc_metadata.csv = cleaned epmc full relevant metadata
- data/epmc_authors.csv = cleaned epmc metadata author information
- data/log_files = folder containing log files for the API calls

---

### 4. Run Analysis and Visualisation
Open notebooks/analysis.ipynb in VSCode or Jupyter Notebooks and run the entire code.
This notebook runs basic statistical analysis on the publication metadata using the clean CSV files.
Visualisations are also produced to show trends in publications and map top authors and affiliations.
Outputs are stored in the output/ folder.
Outputs include:
- CSV files of top publishing authors/affiliations/journals/author collaborations
- Key visualisations:
    1. Article Trends Over Time – Shows growth in PDB-linked publications across the past 5 years.
    2. Distribution of Publications Across Authors and Affliliations
    3. Author Network Mapping Top Publishing Authors and Their Connections
    4. Valid ORCID Coverage Among Authors

---

## Data Sources
PDBe via EBI Search API:
https://www.ebi.ac.uk/ebisearch/ws/rest/pdbe

Europe PMC REST API:
https://europepmc.org/RestfulWebService

---

## Assumptions & Notes
- Only PDB entries deposited between 2020–2025 were queried.
- Linked articles may include older publications due to retrospective citations.
- Journal and affiliation names were not normalised; each variation was treated as a distinct entity, regardless of abbreviations or formatting inconsistencies.
- Author names without a valid ORCID were assumed to represent multiple individuals and were therefore excluded from the analysis of top authors.

---

## Dependencies
See environment.yml for full details. Major packages include:

Python 3.13,
pandas, matplotlib,
requests (for API calls)
notebook, ipykernel (for Jupyter use)

---

## Contact
For questions or feedback, please contact:
Amy Duguid
amyduguid2@gmail.com