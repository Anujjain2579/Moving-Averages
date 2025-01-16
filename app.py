import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf

# Function to fetch stock data
def get_stock_data(symbol, ma_days, ma_weights):
    stock = yf.Ticker(symbol)
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=400)  # Get more than 1 year of data for rolling windows
        price_data = stock.history(start=start_date, end=end_date)

        if price_data.empty:
            return None, None

        # Calculate moving averages dynamically based on user input
        ma_columns = {}
        for days in ma_days:
            column_name = f"{days} Day MA"
            price_data[column_name] = price_data['Close'].rolling(window=days).mean()
            ma_columns[column_name] = {'value': price_data[column_name].iloc[-1], 'broken': 'No'}

        latest_data = price_data.iloc[-1]
        current_price = latest_data['Close']

        # Determine highest order of MA broken and trend direction
        highest_ma_broken = 'None'
        trend = "Neutral"  # Default to neutral trend
        trend_color = "#d3d3d3"

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
        score = 0  # Start with neutral score
        for ma_name, weight in ma_weights.items():
            if ma_columns.get(ma_name, {}).get('broken') == 'Yes':
                if trend == "Upward":
                    score += weight
                elif trend == "Downward":
                    score -= weight

        result_data = {
            'Symbol': symbol.removesuffix(".NS"),
            'Latest Price': current_price,
            'Above/Below All': above_below,
            'Score': score,
            'Trend': trend,
            '_trend_color': trend_color  # Keep as last column
        }
        for ma_name in ma_columns:
            result_data[ma_name] = ma_columns[ma_name]['broken']

        return price_data, result_data
    except Exception as e:
        st.error(f"Error processing symbol {symbol}: {e}")
        return None, None

# Streamlit app
def main():
    st.title("Stock Moving Average Breakout Analysis")

    # Sidebar input
    st.sidebar.subheader("Upload or Enter Tickers")
    uploaded_file = st.sidebar.file_uploader("Upload CSV with 'symbol' column", type="csv")

    if uploaded_file is not None:
        # Read uploaded CSV
        df = pd.read_csv(uploaded_file)
        if 'symbol' not in df.columns:
            st.error("Uploaded CSV must have a 'symbol' column.")
            return
        symbols = [symbol.strip().upper() + '.NS' for symbol in df['symbol']]
    else:
        # Manual input
        symbols_input = st.sidebar.text_input("Enter stock symbols (comma-separated)", value="ARVIND,TRENT,LT,SBIN,PHARMABEES,ULTRACEMCO,AXISBANK,BHARTIARTL,ZOMATO,PAYTM,OFSS,INDIGO,HAL,PERSISTENT,POLYCAB,BSE,MTNL,CDSL,NUVAMA,APARINDS,TECHNOE,TRIVENI,360ONE,JYOTISTRUC,CONCORDBIO,ZENTEC,GOLDIAM,GRAVITA,NEWGEN,ZAGGLE")
        symbols = [symbol.strip().upper() + '.NS' for symbol in symbols_input.split(',')]

    # Moving averages selection
    st.sidebar.subheader("Moving Averages Settings")
    ma_days = st.sidebar.text_input("Enter MA Days (comma-separated, e.g., 200,50,20)", value="200,50,20")
    ma_days = sorted([int(x.strip()) for x in ma_days.split(',') if x.strip().isdigit()], reverse=True)

    # Scoring weights
    st.sidebar.subheader("Scoring Weights")
    default_weights = [50, 30, 20]  # Default weights for top 3 MAs
    ma_weights = {}
    for i, days in enumerate(ma_days):
        default_value = default_weights[i] if i < len(default_weights) else 10
        ma_weights[f"{days} Day MA"] = st.sidebar.number_input(f"{days} Day MA Weight", min_value=0, max_value=100, value=default_value)

    # Fetch data and process
    results = []
    for symbol in symbols:
        _, result = get_stock_data(symbol, ma_days, ma_weights)
        if result:
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
