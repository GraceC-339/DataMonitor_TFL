import requests
import pandas as pd
import streamlit as st
import datetime

# --- CONFIGURATION & UI ---
st.set_page_config(page_title="PFI Infrastucture Monitor", layout="wide")
st.title("PFI Infrastructure Monitor")
st.write(f"**Last Refreshed:** {datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')}")

# --- 1. EXTRACT (API CALL) ---
@st.cache_data(ttl=60) # Cache the data for 60 seconds to avoid excessive API calls during development
def get_tfl_data():
    # API endpoint showing the status of all tube and DLR lines
    URL= "https://api.tfl.gov.uk/Line/Mode/tube,dlr/Status"

    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from API. Status code: {response.status_code}")


# --- 2. TRANSFORM (Business Logic) ---
def transform_data(data):
    # Create a list to hold the transformed data
    incidents = []

    # Loop through each line in the data
    for line in data:
        line_name = line['name']
        line_status = line['lineStatuses'][0]['statusSeverityDescription']

        #Business Logic: If the line status is not "Good Service", we consider it an 'contractual incident'
        is_delayed = 1 if line_status != "Good Service" else 0
        penalty_risk = 100 if is_delayed else 0  # Assuming a fixed penalty fee for simplicity

        # Append the incident information to the list
        incidents.append({
            'Infrastructure Asset': line_name,
            'Current Status': line_status,
            'Compliance Failure': "Yes" if is_delayed else "No",
            'Financial Risk (£)': penalty_risk
        })

    return pd.DataFrame(incidents) # Convert the list of incidents to a pandas DataFrame

# --- 3. LOAD (Data Visualization) ---
try:
    raw_data = get_tfl_data() # Step 1: Extract
    df = transform_data(raw_data) # Step 2: Transform

    # --- TOP ROW METRICS ---
    col1, col2, col3 = st.columns(3)
    total_risk = df['Financial Risk (£)'].sum()
    failure_count = (df['Compliance Failure'] == "Yes").sum()

    col1.metric("Total Assets Monitored", len(df))
    col2.metric("Contractual Incidents", failure_count, delta=f"{failure_count} incidents", delta_color="inverse")
    col3.metric("Total Financial Risk (£)", f"£{total_risk}")

    st.divider() # Visual separator

    # --- CHARTS & TABLES ---
    left_chart, right_table = st.columns([1,1])

    with left_chart:
        st.subheader("Risk Distribution")
        # Creating a simple bar chart of risks
        st.bar_chart(df.set_index("Infrastructure Asset")['Financial Risk (£)'])

    with right_table:
        st.subheader("Asset Status Details")
        st.dataframe(df, use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Error fetching or processing data: {e}")


