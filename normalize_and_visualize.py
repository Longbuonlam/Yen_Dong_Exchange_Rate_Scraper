import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

def normalize_and_visualize():
    # Load CSV files
    usd_vnd = pd.read_csv('usd_vnd_exchange_rates.csv')
    usd_jpy = pd.read_csv('usd_jpy_exchange_rates.csv')

    # Convert 'Date' to datetime for better plotting
    usd_vnd['Date'] = pd.to_datetime(usd_vnd['Date'])
    usd_jpy['Date'] = pd.to_datetime(usd_jpy['Date'])

    # Initialize the scaler
    scaler = MinMaxScaler()

    # Normalize the 'Rate' column for each DataFrame
    usd_vnd['Normalized_Rate'] = scaler.fit_transform(usd_vnd[['Rate']])
    usd_jpy['Normalized_Rate'] = scaler.fit_transform(usd_jpy[['Rate']])

    # Plot normalized rates
    plt.figure(figsize=(12, 6))
    plt.plot(usd_vnd['Date'], usd_vnd['Normalized_Rate'], label='USD to VND', alpha=0.7)
    plt.plot(usd_jpy['Date'], usd_jpy['Normalized_Rate'], label='USD to JPY', alpha=0.7)

    # Customize the plot
    plt.title('Normalized Exchange Rates Over Time')
    plt.xlabel('Date')
    plt.ylabel('Normalized Rate')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Plot histograms of normalized rates
    plt.figure(figsize=(12, 6))
    plt.hist(usd_vnd['Normalized_Rate'], bins=50, alpha=0.5, label='USD to VND')
    plt.hist(usd_jpy['Normalized_Rate'], bins=50, alpha=0.5, label='USD to JPY')

    # Customize the plot
    plt.title('Distribution of Normalized Exchange Rates')
    plt.xlabel('Normalized Rate')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()

    # Save the normalized data back to CSV files
    usd_vnd.to_csv('normalized_usd_vnd_exchange_rates.csv', index=False)
    usd_jpy.to_csv('normalized_usd_jpy_exchange_rates.csv', index=False)

if __name__ == "__main__":
    normalize_and_visualize()
