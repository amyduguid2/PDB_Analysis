# src/fetch_pdb.py
#import required libraries
import time
import requests #used for making HTTP requests to the PDB API

#function to fetch PDB entries from the last 5 years
#This function retrieves PDB entries released between start and end years.
def fetch_pdb_entries(start_year=2019, end_year=2024, log_file="data/fetch_pdb_log.txt"):
    #specify the URL for the PDB API endpoint
    url = "https://www.ebi.ac.uk/ebisearch/ws/rest/pdbe"
    #specify that we want the response in JSON format
    headers = {"Accept": "application/json"}
    #create empty list to store the results
    results = [] 

    #open the log file to write the fetched entries
    with open(log_file, "w") as log:
        for year in range(start_year, end_year + 1):
            print(f"Fetching entries for year: {year}")
            log.write(f"Fetching entries for year: {year}\n")
            start = 0  #starting index for pagination
            size = 1000
            filter = f'creation_date:["{year}/01/01" TO "{year}/12/31"]'  #number of entries to fetch per request
            #loop to fetch all entries for the current year in batches

            hit_count = None

            while True:
                # Stop paginating if we already know start is past the end
                if hit_count is not None and start >= hit_count:
                    break
                
                params = {
                    "query": "*:*",   #fetch all entries           
                    "start": start,   #starting index
                    "size": size,     #fetch 1000 entries per request
                    "format": "json", #specifying the format of the response
                    "fields": "id,description,title,GEO,PUBMED,acc,domain_source,name,creation_date",  #fields to include in the response
                    "filter": filter  #filter to fetch entries created in the specified year
                }
                
                retries = 0
                success = False

                while retries < 3 and not success:
                
                    #handling the response
                    try:
                        #making the GET request to the PDB API
                        response = requests.get(url, params=params, headers=headers, timeout=10)
                        
                        if response.status_code == 200: #check if the request was successful
                            data = response.json() #parse the JSON response
                            if hit_count is None:
                                hit_count = int(data.get("hitCount", 0))
                            entries = data.get('entries', []) #extract the entries from the response
                            if not entries: #if no entries are returned, break the loop 
                                break   
                            results.extend(entries) #add the fetched entries to the results list
                            log.write(f"Fetched {len(entries)} entries for year {year}, start index {start}.\n")
                            print(f"Fetched {len(entries)} entries for year {year}, start index {start}.")
                            success = True
                        else: #error handling for unsuccessful requests
                            log.write(f"Error {response.status_code} for year {year}, start {start}: {response.text}\n")
                            print(f"Error {response.status_code} for year {year}, start {start}: {response.text}")
                            break
                    
                    #handle any exceptions that may occur during the request
                    except requests.exceptions.RequestException as e:
                        retries += 1
                        log.write(f"Retry {retries}/3 failed for year {year}, start {start}: {e}\n")
                        log.write("Retrying in 5 seconds...\n")
                        print(f"Retry {retries}/3 failed for year {year}, start {start}: {e}")
                        print("Retrying in 5 seconds...")
                        time.sleep(5)  #wait 5 seconds and retry the request
                        continue  # retry the loop

                if not success:
                    log.write(f"Failed to fetch data for year {year}, start {start} after 3 retries.\n")
                    print(f"Failed to fetch data for year {year}, start {start} after 3 retries.")
                    break  # Skip to next year if repeated failures

                #increment the starting index for the next batch of entries
                start += size   

    return results