import requests
import json
import os

API_KEY = os.getenv('API_KEY')
DAILY_LIMIT = 25

DATA_DIR = 'data'

PROGRESS_FILE = 'fetched_symbols.json'

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def fetch_cash_flow(symbol):
    url = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey={API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "symbol" in data: 
            save_to_file(symbol, data)
        else:
            print(f"Error fetching data for {symbol}: {data.get('Note', 'No valid data')}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {symbol}: {e}")

def save_to_file(symbol, data):
    file_path = os.path.join(DATA_DIR, f"{symbol}.json")
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data for {symbol} saved to {file_path}")

def save_progress(fetched_symbols):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(fetched_symbols, f)

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return []

def fetch_from_list(stock_symbols):
    fetched_symbols = load_progress()

    remaining_symbols = [symbol for symbol in stock_symbols if symbol not in fetched_symbols]

    if not remaining_symbols:
        print("All symbols fetched. Starting the list over to ensure up-to-date data.")
        fetched_symbols = []
        remaining_symbols = stock_symbols

    symbols_to_fetch = remaining_symbols[:DAILY_LIMIT]

    for symbol in symbols_to_fetch:
        fetch_cash_flow(symbol)
        fetched_symbols.append(symbol)

    save_progress(fetched_symbols)

    print(f"Fetched {len(symbols_to_fetch)} symbols today. Remaining: {len(remaining_symbols) - len(symbols_to_fetch)}")

if __name__ == "__main__":
    stock_symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'V', 'AMZN'] 
    
    fetch_from_list(stock_symbols)
