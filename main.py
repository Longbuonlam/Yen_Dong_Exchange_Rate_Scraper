import requests
import pandas as pd
from datetime import datetime, timedelta
import argparse
import os
from dotenv import load_dotenv

load_dotenv() 

# Load Wise API token from environment variable
API_TOKEN = os.getenv('WISE_API_TOKEN')

if not API_TOKEN:
    print("Error: WISE_API_TOKEN environment variable not set.")
    exit(1)

# Define headers for authentication
headers = {
    'Authorization': f'Bearer {API_TOKEN}'
}

# Initialize a list to store the data
data = [] # Ensure data list is initialized

# --- New code for argument parsing and date calculation ---
parser = argparse.ArgumentParser(description="Fetch exchange rates for a given currency pair for the previous day.")
parser.add_argument("--source", required=True, help="Source currency (e.g., JPY)")
parser.add_argument("--target", required=True, help="Target currency (e.g., VND)")
args = parser.parse_args()

source_currency = args.source.upper()
target_currency = args.target.upper()

# Calculate "yesterday" based on the script's execution time (UTC in GitHub Actions)
date_to_fetch = datetime.utcnow() - timedelta(days=1)

# Format the date as ISO 8601
date_str_api = date_to_fetch.strftime('%Y-%m-%dT00:00:00Z') # For the API
date_str_file = date_to_fetch.strftime('%d-%m-%Y') # For the filename

# Define the API endpoint with query parameters
url = f'https://api.transferwise.com/v1/rates?source={source_currency}&target={target_currency}&time={date_str_api}'

# Make the API request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    rates_data = response.json()
    if rates_data:
        rate_info = rates_data[0]
        data.append({
            'Date': date_to_fetch.strftime('%Y-%m-%d'),
            'Rate': rate_info['rate']
        })
    else:
        print(f"No rate data found for {source_currency}/{target_currency} on {date_to_fetch.strftime('%Y-%m-%d')}")
else:
    print(f"Failed to fetch data for {source_currency}/{target_currency} on {date_to_fetch.strftime('%Y-%m-%d')}. Status: {response.status_code}, Response: {response.text}")

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
csv_filename = f"{source_currency.lower()}_{target_currency.lower()}_exchange_rates({date_str_file}).csv"

if not df.empty:
    df.to_csv(csv_filename, index=False)
    print(f"✅ Exchange rate data saved to '{csv_filename}'")
else:
    print(f"No data fetched for {source_currency}/{target_currency} on {date_to_fetch.strftime('%Y-%m-%d')}, CSV not created.")

