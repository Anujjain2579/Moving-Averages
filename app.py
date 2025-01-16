import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf

# Function to fetch stock data
def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=400)  # Get more than 1 year of data for rolling windows
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

        # Determine highest order of MA broken and trend direction
        highest_ma_broken = 'None'
        trend = "Neutral"  # Default to neutral trend
        trend_color = "#d3d3d3"

        # Check moving averages in descending order of importance
        if not np.isnan(latest_data['200_SMA']):
            prev_2_data = price_data.iloc[-3:]['Close']  # Check last 3 days' closing prices
            if (prev_2_data.iloc[-1] > latest_data['200_SMA']) and (prev_2_data.iloc[-2] <= latest_data['200_SMA']):
                highest_ma_broken = '200 Day MA'
                trend = "Upward"
                trend_color = "green"
            elif (prev_2_data.iloc[-1] < latest_data['200_SMA']) and (prev_2_data.iloc[-2] >= latest_data['200_SMA']):
                highest_ma_broken = '200 Day MA'
                trend = "Downward"
                trend_color = "red"

        if highest_ma_broken == 'None' and not np.isnan(latest_data['100_SMA']):
            if (prev_2_data.iloc[-1] > latest_data['100_SMA']) and (prev_2_data.iloc[-2] <= latest_data['100_SMA']):
                highest_ma_broken = '100 Day MA'
                trend = "Upward"
                trend_color = "green"
            elif (prev_2_data.iloc[-1] < latest_data['100_SMA']) and (prev_2_data.iloc[-2] >= latest_data['100_SMA']):
                highest_ma_broken = '100 Day MA'
                trend = "Downward"
                trend_color = "red"

        if highest_ma_broken == 'None' and not np.isnan(latest_data['50_SMA']):
            if (prev_2_data.iloc[-1] > latest_data['50_SMA']) and (prev_2_data.iloc[-2] <= latest_data['50_SMA']):
                highest_ma_broken = '50 Day MA'
                trend = "Upward"
                trend_color = "green"
            elif (prev_2_data.iloc[-1] < latest_data['50_SMA']) and (prev_2_data.iloc[-2] >= latest_data['50_SMA']):
                highest_ma_broken = '50 Day MA'
                trend = "Downward"
                trend_color = "red"

        if highest_ma_broken == 'None' and not np.isnan(latest_data['20_SMA']):
            if (prev_2_data.iloc[-1] > latest_data['20_SMA']) and (prev_2_data.iloc[-2] <= latest_data['20_SMA']):
                highest_ma_broken = '20 Day MA'
                trend = "Upward"
                trend_color = "green"
            elif (prev_2_data.iloc[-1] < latest_data['20_SMA']) and (prev_2_data.iloc[-2] >= latest_data['20_SMA']):
                highest_ma_broken = '20 Day MA'
                trend = "Downward"
                trend_color = "red"
        return price_data, {
            'Symbol': symbol.removesuffix(".NS"),
            'Latest Price': current_price,
            'Highest Order of MA Broken': highest_ma_broken,
            'Trend': trend,
            'Trend Color': trend_color
        }
    except Exception as e:
        st.error(f"Error processing symbol {symbol}: {e}")
        return None, None

# Streamlit app
def main():
    st.title("Stock Moving Average Breakout Analysis")

    # Sidebar input
    symbols_input = st.sidebar.text_input("Enter stock symbols (comma-separated)", value="BSE,ADANIGREEN")
    symbols = [symbol.strip().upper() for symbol in symbols_input.split(',')]

    # Fetch data and process
    results = []
    for symbol in symbols:
        symbol += '.NS'
        _, result = get_stock_data(symbol)
        if result:
            results.append(result)

    # Display results
    if results:
        results_df = pd.DataFrame(results)
        st.subheader("Stock Signals")

        # Highlight based on trend color
        def highlight_trend(row):
            color = row['Trend Color']
            return [f'background-color: {color}' for _ in row]
        
        styled_df = results_df.drop(columns=['Trend Color'])
        styled_df = results_df.style.apply(highlight_trend, axis=1)
        st.dataframe(styled_df, use_container_width=True)

if __name__ == "__main__":
    main()
