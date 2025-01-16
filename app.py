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
        price_data['200_SMA'] = price_data['Close'].rolling(window=200).mean()

        latest_data = price_data.iloc[-1]
        current_price = latest_data['Close']

        # Determine highest order of MA broken and trend direction
        highest_ma_broken = 'None'
        trend = "Neutral"  # Default to neutral trend
        trend_color = "#d3d3d3"
        ma_columns = {
            '200 Day MA': {'value': latest_data['200_SMA'], 'broken': 'No'},
            '50 Day MA': {'value': latest_data['50_SMA'], 'broken': 'No'},
            '20 Day MA': {'value': latest_data['20_SMA'], 'broken': 'No'}
        }

        # Check moving averages individually
        for ma_name, details in ma_columns.items():
            if not np.isnan(details['value']):
                prev_2_data = price_data.iloc[-3:]['Close']
                if (prev_2_data.iloc[-1] > details['value']) and (prev_2_data.iloc[-2] <= details['value']):
                    details['broken'] = 'Yes'
                    highest_ma_broken = ma_name
                    trend = "Upward"
                    trend_color = "green"
                elif (prev_2_data.iloc[-1] < details['value']) and (prev_2_data.iloc[-2] >= details['value']):
                    details['broken'] = 'Yes'
                    highest_ma_broken = ma_name
                    trend = "Downward"
                    trend_color = "red"
                else:
                    details['broken'] = 'No'

        # Check if stock is above or below all MAs
        above_below = "-"
        if all(current_price > details['value'] for details in ma_columns.values() if not np.isnan(details['value'])):
            above_below = "Above All"
        elif all(current_price < details['value'] for details in ma_columns.values() if not np.isnan(details['value'])):
            above_below = "Below All"   

        # Scoring system: +100 to -100
        weights = {'200 Day MA': 50, '50 Day MA': 15, '20 Day MA': 10}
        score = 0  # Start with neutral score
        for ma_name, weight in weights.items():
            if ma_columns[ma_name]['broken'] == 'Yes':
                if trend == "Upward":
                    score += weight
                elif trend == "Downward":
                    score -= weight

        return price_data, {
            'Symbol': symbol.removesuffix(".NS"),
            'Latest Price': current_price,
            '200 Day MA': ma_columns['200 Day MA']['broken'],
            '50 Day MA': ma_columns['50 Day MA']['broken'],
            '20 Day MA': ma_columns['20 Day MA']['broken'],
            'Above/Below All': above_below,
            'Score': score,
            'Trend': trend,
            '_trend_color': trend_color  # Keep as last column
        }
    except Exception as e:
        st.error(f"Error processing symbol {symbol}: {e}")
        return None, None

# Streamlit app
def main():
    st.title("Stock Moving Average Breakout Analysis")

    # Sidebar input
    symbols_input = st.sidebar.text_input("Enter stock symbols (comma-separated)", value="KALYANKJIL,BIOCON,EICHERMOT,TRENT,LT,SBIN,PHARMABEES,ULTRACEMCO,AXISBANK,BHARTIARTL,ZOMATO,PAYTM,OFSS,INDIGO,HAL,PERSISTENT,POLYCAB,BSE,MTNL,CDSL,NUVAMA,APARINDS,TECHNOE,TRIVENI,360ONE,JYOTISTRUC,CONCORDBIO,ZENTEC,GOLDIAM,GRAVITA,NEWGEN,ZAGGLE")
    symbols = [symbol.strip().upper() + '.NS' for symbol in symbols_input.split(',')]

    # Scoring weights
    st.sidebar.subheader("Scoring Weights")
    weights = {
        '200 Day MA': st.sidebar.number_input("200 Day MA Weight", min_value=0, max_value=100, value=50),
        '50 Day MA': st.sidebar.number_input("50 Day MA Weight", min_value=0, max_value=100, value=15),
        '20 Day MA': st.sidebar.number_input("20 Day MA Weight", min_value=0, max_value=100, value=10)
    }

    # Fetch data and process
    results = []
    for symbol in symbols:
        _, result = get_stock_data(symbol)
        if result:
            # Adjust scores based on user weights
            result['Score'] = 0
            for ma_name, weight in weights.items():
                if result[ma_name] == 'Yes':
                    if result['Trend'] == "Upward":
                        result['Score'] += weight
                    elif result['Trend'] == "Downward":
                        result['Score'] -= weight
            results.append(result)

    # Display results
    if results:
        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values(by='Score', key=abs, ascending=False).reset_index(drop=True)
        st.subheader("Stock Signals")

        # Extract trend colors before dropping the column
        trend_colors = results_df['_trend_color']
        
        # Remove the internal color column
        results_df = results_df.drop('_trend_color', axis=1)

        # Modified highlight function to use the stored colors
        def highlight_trend(row):
            color = trend_colors[row.name]
            return [f'background-color: {color}' for _ in row]

        styled_df = results_df.style.apply(highlight_trend, axis=1)
        st.dataframe(styled_df, use_container_width=True)

if __name__ == "__main__":
    main()
