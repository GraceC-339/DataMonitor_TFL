# DataMonitor TFL

A Streamlit dashboard that monitors the real-time status of Transport for London (TFL) tube and DLR lines and highlights contractual incident risk.

## Overview

This project fetches live service status data from the TFL API, transforms it to flag lines that are not running a "Good Service", and calculates a financial risk value for each incident. The results are displayed in an interactive dashboard.

## How It Works

1. **Extract** - Calls the TFL API endpoint for tube and DLR line statuses.
2. **Transform** - Loops through each line and applies business logic:
   - If a line's status is anything other than `"Good Service"`, it is flagged as a compliance failure (`"Yes"`) and assigned a financial risk of £100.
   - Lines running normally receive `"No"` and `£0` risk.
3. **Load (Dashboard)** - Displays:
   - Top metrics for total assets monitored, contractual incidents, and total financial risk.
   - A bar chart showing risk distribution by infrastructure asset.
   - A detailed status table for all assets.

Data is cached for 60 seconds using Streamlit cache (`@st.cache_data(ttl=60)`) to reduce repeated API calls.

## Requirements

- Python 3.x
- [requests](https://pypi.org/project/requests/)
- [pandas](https://pypi.org/project/pandas/)

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal (typically `http://localhost:8501`).

The dashboard uses a DataFrame with the following columns:

| Column | Description |
|---|---|
| `Infrastructure Asset` | Name of the tube or DLR line |
| `Current Status` | Current service status description |
| `Compliance Failure` | `"Yes"` if the line is not running a Good Service, otherwise `"No"` |
| `Financial Risk (£)` | Financial risk in £ (£100 per incident, £0 otherwise) |

## Data Source

Live data is sourced from the [TFL Unified API](https://api.tfl.gov.uk/):

```
https://api.tfl.gov.uk/Line/Mode/tube,dlr/Status
```
