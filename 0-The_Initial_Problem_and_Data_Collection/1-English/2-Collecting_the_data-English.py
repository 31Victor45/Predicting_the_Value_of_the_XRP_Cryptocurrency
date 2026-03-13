import yfinance as yf
import pandas as pd

def extract_clean_data(end_date="2026-03-11"):
    ticker_symbol = "XRP-USD"
    print(f"Downloading {ticker_symbol} clean data...")

    # 1. Standard download
    df = yf.download(ticker_symbol, period="max", end=end_date, actions=True)

    # 2. CORRECTION: If the DataFrame has MultiIndex columns, flatten them
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # 3. Clean column names
    # This removes extra spaces and ensures 'Date' becomes a column
    df = df.reset_index()
    
    # 4. Remove any rows that are fully null or contain repeated column names
    df = df.dropna(subset=['Close']) 

    # 5. Add basic metadata as simple columns
    df['Ticker'] = ticker_symbol
    df['Currency'] = "USD"

    # Reorder for better readability
    cols = ['Date', 'Ticker', 'Currency', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = df[cols]

    # 6. Save without pandas index to avoid 'Unnamed: 0' columns
    file_name = "XRP_Data.csv"
    df.to_csv(file_name, index=False)
    
    print(f"File saved successfully: {file_name}")
    print(df.head())

if __name__ == "__main__":
    extract_clean_data()