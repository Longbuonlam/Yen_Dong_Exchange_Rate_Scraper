import requests
import pandas as pd
from datetime import datetime, timedelta

# Replace with your actual Wise API token
API_TOKEN = 'e10ee85b-1134-40d6-b5da-61449c07bd2b'

# Define headers for authentication
headers = {
    'Authorization': f'Bearer {API_TOKEN}'
}

# Define the start and end dates
start_date = datetime(2020, 4, 16)
end_date = datetime(2025, 4, 15)

# Initialize a list to store the data
data = []

# Loop through each day in the date range
current_date = start_date
while current_date <= end_date:
    # Format the date as ISO 8601
    date_str = current_date.strftime('%Y-%m-%dT00:00:00Z')
    
    # Define the API endpoint with query parameters
    url = f'https://api.transferwise.com/v1/rates?source=JPY&target=VND&time={date_str}'
    
    # Make the API request
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        rates = response.json()
        if rates:
            rate_info = rates[0]
            data.append({
                'Date': current_date.strftime('%Y-%m-%d'),
                'Rate': rate_info['rate']
            })
    else:
        print(f"Failed to fetch data for {current_date.strftime('%Y-%m-%d')}")
    
    # Move to the next day
    current_date += timedelta(days=1)

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('jpy_vnd_exchange_rates.csv', index=False)

print("✅ Exchange rate data saved to 'jpy_vnd_exchange_rates.csv'")

