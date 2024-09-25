# python libary to download
import requests
import matplotlib.pyplot as plt
import pandas as pd

# Your API key for accessing the stock data service
API_KEY = '2ad2a1d66a584c298d5b0d29c315334c'

# Function to get stock data for the last 7 days
def get_stock_data(symbol):
    url = f'https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize=7&apikey={API_KEY}'
    response = requests.get(url) #it will go to the url and see the data 
    data = response.json() # it is colleting the data
    
    # Check for errors in the response {it is for the website error}
    if 'values' not in data:
        print(f"Error fetching data for {symbol}. Please check the stock symbol.")
        return None
    #data means the data obtain from the api 
    return data

# Function to process stock data (Date, Open, High, Low, Close)
def process_stock_data(data):
    dates = []             # dates
    open_prices = []       #opeining price of the stock in that date
    high_prices = []       #high price of the stock in that date
    low_prices = []        #low price of the stock in that date
    closing_prices = []    #closing price of the stock in that date
    
    for item in data.get('values', []):
        #fetching the data from the api 
        dates.append(item['datetime'])
        open_prices.append(float(item['open']))
        high_prices.append(float(item['high']))
        low_prices.append(float(item['low']))
        closing_prices.append(float(item['close']))
    
    return dates, open_prices, high_prices, low_prices, closing_prices

# Option A: Get the stock data of one stock for the past week (Open, High, Low, Close)
def option_a():
    symbol = input("Enter the stock symbol (e.g., AAPL for Apple,GOOG for Google): ").upper()
    data = get_stock_data(symbol)
    
    if data:
        dates, open_prices, high_prices, low_prices, closing_prices = process_stock_data(data)
        
        # Create a DataFrame to display the data nicely
        stock_df = pd.DataFrame({
            'Date': dates,
            'Open': open_prices,
            'High': high_prices,
            'Low': low_prices,
            'Close': closing_prices
        })
        print(stock_df)
        
        # Plot the closing prices
        plt.figure(figsize=(10, 6))
        plt.plot(dates, closing_prices, marker='o', linestyle='-', color='orange', label=f'Closing Price')
        plt.plot(dates, open_prices, marker='o', linestyle='-', color='g', label='Open Price')
        plt.plot(dates, high_prices, marker='o', linestyle='-', color='r', label='High Price')
        plt.plot(dates, low_prices, marker='o', linestyle='-', color='b', label='Low Price')
        
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.title(f'{symbol} Stock Prices (Last 7 Days)')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

 # Option B: Compare two stocks and plot their closing prices
def option_b():
    symbol1 = input("Enter the first stock symbol e.g., AAPL for Apple: ").upper()
    symbol2 = input("Enter the second stock symbol e.g.,GOOG for Google: ").upper()
    
    # Fetch data for the first stock
    data1 = get_stock_data(symbol1)
    if not data1:
        print(f"Failed to fetch data for {symbol1}. Please check the stock symbol and try again.")
        return
    
    # Fetch data for the second stock
    data2 = get_stock_data(symbol2)
    if not data2:
        print(f"Failed to fetch data for {symbol2}. Please check the stock symbol and try again.")
        return
    
    
    # Process stock data for both stocks (extract dates and closing prices)
    dates1, _, _, _, closing_prices1 = process_stock_data(data1)  # Use '_' for unused values
    dates2, _, _, _, closing_prices2 = process_stock_data(data2)
    
    # Check if both stocks have the same dates for comparison
    if dates1 != dates2:
        print("Warning: The two stocks have different date ranges. Plotting data might not be fully aligned.")
    
    # Plot the closing prices of both stocks
    plt.figure(figsize=(10, 6))
    plt.plot(dates1, closing_prices1, marker='o', linestyle='-', color='b', label=f'{symbol1} Closing Price')
    plt.plot(dates2, closing_prices2, marker='o', linestyle='-', color='r', label=f'{symbol2} Closing Price')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.title(f'Comparison of {symbol1} and {symbol2} Closing Prices (Last 7 Days)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()


# Option C: Save the stock data (Open, High, Low, Close) to CSV
def option_c():
    symbol = input("Enter the stock symbol (e.g., AAPL for Apple,GOOG for Google): ").upper()
    data = get_stock_data(symbol)
    
    if data:
        dates, open_prices, high_prices, low_prices, closing_prices = process_stock_data(data)
        
        # Create a DataFrame
        stock_df = pd.DataFrame({
            'Date': dates,
            'Open': open_prices,
            'High': high_prices,
            'Low': low_prices,
            'Close': closing_prices
        })
        
        # Save the DataFrame to CSV
        stock_df.to_csv(f"{symbol}_stock_report.csv", index=False, encoding='utf-8')
        print(f"{symbol}_stock_report.csv has been created successfully!")

# Main menu to choose between options
def main():
    print("""
         _             _            _                        
     ___| |_ ___   ___| | __ __   _(_) _____      _____ _ __ 
    / __| __/ _ \ / __| |/ / \ \ / / |/ _ \ \ /\ / / _ \ '__|
    \__ \ || (_) | (__|   <   \ V /| |  __/\ V  V /  __/ |   
    |___/\__\___/ \___|_|\_\   \_/ |_|\___| \_/\_/ \___|_|   
     """)
    print("Choose an option:")
    print("a) Get the stock data of the last week (Open, High, Low, Close)")
    print("b) Compare two stocks and plot their closing prices")
    print("c) Save the stock data (Open, High, Low, Close) to CSV")
    
    choice = input("Enter your choice (a/b/c): ").lower()
    
    if choice == 'a':
        option_a()
    elif choice == 'b':
        option_b()
    elif choice == 'c':
        option_c()
    else:
        print("Invalid choice. Please select a, b, or c.")

# Run the main function
main()

       
