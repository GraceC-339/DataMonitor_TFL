import requests
import pandas as pd

# API endpoint showing the status of all tube and DLR lines
URL= "https://api.tfl.gov.uk/Line/Mode/tube,dlr/Status"

#1. Extracting the data from the API and converting it to a pandas dataframe
def extract_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from API. Status code: {response.status_code}")

# Run the extraction function
raw_json = extract_data(URL)

# 2. Transforming the data (business logic)
def transform_data(data):
    # Create a list to hold the transformed data
    incidents = []

    # Loop through each line in the data
    for line in data:
        line_name = line['name']
        line_status = line['lineStatuses'][0]['statusSeverityDescription']

        #Business Logic: If the line status is not "Good Service", we consider it an 'contractual incident'
        is_penalty = 1 if line_status != "Good Service" else 0
        penalty_fee = 100 if is_penalty else 0  # Assuming a fixed penalty fee for simplicity

        # Append the incident information to the list
        incidents.append({
            'line_name': line_name,
            'line_status': line_status,
            'is_penalty': is_penalty,
            'penalty_fee': penalty_fee
        })

    return pd.DataFrame(incidents) # Convert the list of incidents to a pandas DataFrame

# Run the transformation function
transformed_data = transform_data(raw_json)  

