import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import yfinance as yf

# Function to fetch stock data
def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)  # Get 1 year of data
        price_data = stock.history(start=start_date, end=end_date)

        if price_data.empty:
            return None, None

        # Calculate moving averages
        price_data['20_SMA'] = price_data['Close'].rolling(window=20).mean()
        price_data['50_SMA'] = price_data['Close'].rolling(window=50).mean()
        price_data['100_SMA'] = price_data['Close'].rolling(window=100).mean()
        price_data['200_SMA'] = price_data['Close'].rolling(window=200).mean()

        latest_data = price_data.iloc[-1]
        current_price = latest_data['Close']

        # Determine if the stock has broken the moving averages
        signals = {
            '200_SMA_Broken': current_price > latest_data['200_SMA'],
            '100_SMA_Broken': current_price > latest_data['100_SMA'],
            '50_SMA_Broken': current_price > latest_data['50_SMA'],
            '20_SMA_Broken': current_price > latest_data['20_SMA']
        }

        return price_data, {
            'Symbol': symbol,
            'Latest Price': current_price,
            '200 Day MA Broken': 'Yes' if signals['200_SMA_Broken'] else 'No',
            '100 Day MA Broken': 'Yes' if signals['100_SMA_Broken'] else 'No',
            '50 Day MA Broken': 'Yes' if signals['50_SMA_Broken'] else 'No',
            '20 Day MA Broken': 'Yes' if signals['20_SMA_Broken'] else 'No',

            #'100 Day MA Broken': 'Yes' if signals['200_SMA_Broken'] is False and signals['100_SMA_Broken'] else 'No',
            #'50 Day MA Broken': 'Yes' if signals['200_SMA_Broken'] is False and signals['100_SMA_Broken'] is False and signals['50_SMA_Broken'] else 'No',
            #'20 Day MA Broken': 'Yes' if signals['200_SMA_Broken'] is False and signals['100_SMA_Broken'] is False and signals['50_SMA_Broken'] is False and signals['20_SMA_Broken'] else 'No'
        }
    except Exception as e:
        st.error(f"Error processing symbol {symbol}: {e}")
        return None, None

def main():
    st.title("Moving Average Signals")

    # Sidebar for user input
    st.sidebar.header("Stock Input")
    symbols = st.sidebar.text_input("Enter stock symbols (comma-separated)", value="BSE").split(',')

    # Fetch data and process
    results = []
    for symbol in symbols:
        symbol = symbol.strip().upper()
        symbol = symbol +'.NS'
        if symbol:
            _, result = get_stock_data(symbol)
            if result:
                results.append(result)

    # Display results
    if results:
        results_df = pd.DataFrame(results)
        st.subheader("Stock Signals")
        st.dataframe(results_df)

if __name__ == "__main__":
    main()