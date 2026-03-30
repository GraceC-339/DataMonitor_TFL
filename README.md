# DataMonitor TFL

A Python script that monitors the real-time status of Transport for London (TFL) tube and DLR lines and identifies contractual incidents based on service disruptions.

## Overview

This project fetches live service status data from the TFL API, transforms it to flag lines that are not running a "Good Service", and calculates an associated penalty fee for each incident.

## How It Works

1. **Extract** – Calls the TFL API endpoint for tube and DLR line statuses.
2. **Transform** – Loops through each line and applies business logic:
   - If a line's status is anything other than `"Good Service"`, it is flagged as a contractual incident (`is_penalty = 1`) and assigned a penalty fee of £100.
   - Lines running normally receive `is_penalty = 0` and `penalty_fee = 0`.
3. The results are returned as a **pandas DataFrame**.

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
python app.py
```

The script will print/return a DataFrame with the following columns:

| Column | Description |
|---|---|
| `line_name` | Name of the tube or DLR line |
| `line_status` | Current service status description |
| `is_penalty` | `1` if the line is not running a Good Service, otherwise `0` |
| `penalty_fee` | Penalty fee in £ (£100 per incident, £0 otherwise) |

## Data Source

Live data is sourced from the [TFL Unified API](https://api.tfl.gov.uk/):

```
https://api.tfl.gov.uk/Line/Mode/tube,dlr/Status
```
