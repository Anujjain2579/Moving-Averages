import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
from yahooquery import Ticker  # Used to fetch fundamental data
import pytz

NIFTY_TOP_50 = ['ADANIENT.NS', 'ADANIPORTS.NS', 'APOLLOHOSP.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BEL.NS', 'BPCL.NS', 'BHARTIARTL.NS', 'BRITANNIA.NS', 'CIPLA.NS', 'COALINDIA.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'GRASIM.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDUNILVR.NS',
                'ICICIBANK.NS', 'INDUSINDBK.NS', 'INFY.NS', 'ITC.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LT.NS', 'M&M.NS', 'MARUTI.NS', 'NESTLEIND.NS', 'NTPC.NS', 'ONGC.NS', 'POWERGRID.NS', 'RELIANCE.NS', 'SBILIFE.NS', 'SHRIRAMFIN.NS', 'SBIN.NS', 'SUNPHARMA.NS', 'TCS.NS', 'TATACONSUM.NS', 'TATAMOTORS.NS', 'TATASTEEL.NS', 'TECHM.NS', 'TITAN.NS', 'TRENT.NS', 'ULTRACEMCO.NS', 'WIPRO.NS']
NIFTY_NEXT_150 = ['ASTRAL.NS', 'PFC.NS', 'IGL.NS', 'GAIL.NS', 'AUBANK.NS', 'UNITDSPR.NS', 'VEDL.NS', 'LICI.NS', 'ZOMATO.NS', 'INDIANB.NS', 'HDFCAMC.NS', 'CUMMINSIND.NS', 'MAZDOCK.NS', 'ACC.NS', 'DELHIVERY.NS', 'BSE.NS', 'ALKEM.NS', 'BALKRISIND.NS', 'OFSS.NS', 'CGPOWER.NS', 'HUDCO.NS', 'INDUSTOWER.NS', 'ATGL.NS', 'MFSL.NS', 'POLICYBZR.NS', 'PAGEIND.NS', 'CONCOR.NS', 'FEDERALBNK.NS',
                  'GMRAIRPORT.NS', 'TORNTPHARM.NS', 'BAJAJHLDNG.NS', 'EXIDEIND.NS', 'PIDILITIND.NS', 'LICHSGFIN.NS', 'ICICIPRULI.NS', 'ASHOKLEY.NS', 'PNB.NS', 'PAYTM.NS', 'KPITTECH.NS', 'UPL.NS', 'RECLTD.NS', 'IOB.NS', 'INDHOTEL.NS', 'TATAPOWER.NS', 'INDIGO.NS', 'ABCAPITAL.NS', 'MRPL.NS', 'VOLTAS.NS', 'JUBLFOOD.NS', 'PETRONET.NS', 'ICICIGI.NS', 'BHEL.NS', 'APLAPOLLO.NS',
                'ABFRL.NS', 'SBICARD.NS', 'LODHA.NS', 'BHARTIHEXA.NS', 'NAUKRI.NS', 'SAIL.NS', 'SUZLON.NS', 'POLYCAB.NS', 'SUPREMEIND.NS', 'MANKIND.NS', 'CANBK.NS', 'NMDC.NS', 'IDEA.NS', 'MUTHOOTFIN.NS', 'MARICO.NS', 'MAHABANK.NS', 'JIOFIN.NS', 'OBEROIRLTY.NS', 'PERSISTENT.NS', 'OIL.NS', 'COLPAL.NS', 'IRFC.NS', 'ABB.NS', 'FACT.NS', 'IREDA.NS', 'PIIND.NS', 'TATATECH.NS', 'LUPIN.NS',
                  'YESBANK.NS', 'UNIONBANK.NS', 'KALYANKJIL.NS', 'CHOLAFIN.NS', 'COFORGE.NS', 'PHOENIXLTD.NS', 'APOLLOTYRE.NS', 'NHPC.NS', 'JSWINFRA.NS', 'TVSMOTOR.NS', 'ZYDUSLIFE.NS', 'BOSCHLTD.NS', 'GODREJCP.NS', 'HINDPETRO.NS', 'MPHASIS.NS', 'SHREECEM.NS', 'BANKBARODA.NS', 'IOC.NS', 'M&MFIN.NS', 'COCHINSHIP.NS', 'PRESTIGE.NS', 'SUNDARMFIN.NS', 'BHARATFORG.NS', 'PATANJALI.NS',
                    'IRB.NS', 'DABUR.NS', 'JSWENERGY.NS', 'VBL.NS', 'AMBUJACEM.NS', 'POONAWALLA.NS', 'GODREJPROP.NS', 'TIINDIA.NS', 'NYKAA.NS', 'SIEMENS.NS', 'BIOCON.NS', 'MOTHERSON.NS', 'DMART.NS', 'HINDZINC.NS', 'DIXON.NS', 'MRF.NS', 'LTIM.NS', 'MAXHEALTH.NS', 'TATACOMM.NS', 'NLCINDIA.NS', 'BANDHANBNK.NS', 'TATACHEM.NS', 'SRF.NS', 'AUROPHARMA.NS', 'ADANIPOWER.NS', 'JINDALSTEL.NS', 
                    'IDBI.NS', 'RVNL.NS', 'TORNTPOWER.NS', 'HAVELLS.NS', 'IDFCFIRSTB.NS', 'SOLARINDS.NS', 'BDL.NS', 'TATAELXSI.NS', 'ESCORTS.NS', 'DIVISLAB.NS', 'LTF.NS', 'BANKINDIA.NS', 'HAL.NS', 'DLF.NS', 'SONACOMS.NS', 'ADANIENSOL.NS', 'SJVN.NS', 'IRCTC.NS', 'ADANIGREEN.NS']
NIFTY_NEXT_300 = ['IRCON.NS', 'GRAPHITE.NS', 'KSB.NS', 'ACE.NS', 'WHIRLPOOL.NS', 'PTCIL.NS', 'BRIGADE.NS', 'MCX.NS', 'IEX.NS', 'APLLTD.NS', 'BSOFT.NS', 'CAMS.NS', 'ASAHIINDIA.NS', 'HINDCOPPER.NS', 'USHAMART.NS', 'RAINBOW.NS', 'JUSTDIAL.NS', 'LLOYDSME.NS', 'OLECTRA.NS', 'UJJIVANSFB.NS', 'POLYMED.NS', 'UCOBANK.NS', 'VTL.NS', 'CASTROLIND.NS', 'EIDPARRY.NS', 'PVRINOX.NS', 'RKFORGE.NS',
                   'INDIAMART.NS', 'MASTEK.NS', 'ELGIEQUIP.NS', 'AKUMS.NS', 'CERA.NS', 'BATAINDIA.NS', 'WELSPUNLIV.NS', 'METROPOLIS.NS', 'GSFC.NS', 'DOMS.NS', 'FIVESTAR.NS', 'KFINTECH.NS', 'FSL.NS', 'BLS.NS', 'POWERINDIA.NS', 'KAJARIACER.NS', 'MEDANTA.NS', 'TRITURBINE.NS', 'NATIONALUM.NS', 'SIGNATURE.NS', 'TRIVENI.NS', 'NEWGEN.NS', 'KPRMILL.NS', '360ONE.NS', 'JYOTICNC.NS', 'RRKABEL.NS',
                    'SKFINDIA.NS', 'SYRMA.NS', 'ANANTRAJ.NS', 'WESTLIFE.NS', 'SCHNEIDER.NS', 'CAPLIPOINT.NS', 'TEJASNET.NS', 'NETWEB.NS', 'TIMKEN.NS', 'ABBOTINDIA.NS', 'SUMICHEM.NS', 'INOXWIND.NS', 'ANGELONE.NS', 'HSCL.NS', 'ITI.NS', 'TRIDENT.NS', 'GPIL.NS', 'QUESS.NS', 'EMCURE.NS', 'STARHEALTH.NS', 'BIKAJI.NS', 'ALKYLAMINE.NS', 'THERMAX.NS', 'HEG.NS', 'VINATIORGA.NS', 'GICRE.NS', 'BEML.NS',
                    'JUBLINGREA.NS', 'BALRAMCHIN.NS', 'AEGISLOG.NS', 'AAVAS.NS', 'CRAFTSMAN.NS', 'KARURVYSYA.NS', 'ASTRAZEN.NS', 'CHENNPETRO.NS', 'PFIZER.NS', 'INTELLECT.NS', 'EMAMILTD.NS', 'SHYAMMETL.NS', 'LINDEINDIA.NS', 'GODFRYPHLP.NS', 'VIJAYA.NS', 'JKTYRE.NS', 'RATNAMANI.NS', 'PGHH.NS', 'UNOMINDA.NS', 'HAPPSTMNDS.NS', 'DATAPATTNS.NS', 'NATCOPHARM.NS', 'ELECON.NS', 'NSLNISP.NS',
                    'PEL.NS', 'JSL.NS', 'SONATSOFTW.NS', 'CDSL.NS', 'DEVYANI.NS', 'TVSSCS.NS', 'ENDURANCE.NS', 'CEATLTD.NS', 'TITAGARH.NS', 'HONAUT.NS', 'ALOKINDS.NS', 'ZENSARTECH.NS', 'INOXINDIA.NS', 'CONCORDBIO.NS', 'BBTC.NS', 'PCBL.NS', 'BALAMINES.NS', 'IFCI.NS', 'RADICO.NS', 'BAYERCROP.NS', 'TECHNOE.NS', 'LATENTVIEW.NS', 'RTNINDIA.NS', 'MAHLIFE.NS', 'FINEORG.NS', 'AIAENG.NS', 'PNCINFRA.NS',
                    'EIHOTEL.NS', 'EASEMYTRIP.NS', 'MMTC.NS', 'KPIL.NS', 'AJANTPHARM.NS', 'ANANDRATHI.NS', 'UTIAMC.NS', 'SCI.NS', 'GRSE.NS', 'JINDALSAW.NS', '3MINDIA.NS', 'KIRLOSBROS.NS', 'JUBLPHARMA.NS', 'GNFC.NS', 'METROBRAND.NS', 'RITES.NS', 'RAYMOND.NS', 'BASF.NS', 'IIFL.NS', 'GODREJAGRO.NS', 'CHAMBLFERT.NS', 'CHALET.NS', 'CCL.NS', 'AFFLE.NS', 'NIACL.NS', 'SYNGENE.NS', 'SWSOLAR.NS', 'ISEC.NS',
                    'VGUARD.NS', 'MOTILALOFS.NS', 'IPCALAB.NS', 'ZFCVINDIA.NS', 'ACI.NS', 'LALPATHLAB.NS', 'GLAND.NS', 'MANAPPURAM.NS', 'ERIS.NS', 'KNRCON.NS', 'INDGN.NS', 'CRISIL.NS', 'GLENMARK.NS', 'RENUKA.NS', 'CANFINHOME.NS', 'SUNTV.NS', 'CELLO.NS', 'BIRLACORPN.NS', 'INDIACEM.NS', 'GODIGIT.NS', 'MANYAVAR.NS', 'SPARC.NS', 'CARBORUNIV.NS', 'TATAINVEST.NS', 'JBCHEPHARM.NS', 'BLUESTARCO.NS',
                    'APARINDS.NS', 'GVT&D.NS', 'ROUTE.NS', 'CENTRALBK.NS', 'CESC.NS', 'AMBER.NS', 'KEC.NS', 'ABREL.NS', 'MINDACORP.NS', 'ATUL.NS', 'MGL.NS', 'JMFINANCIL.NS', 'SUVENPHAR.NS', 'RAILTEL.NS', 'CAMPUS.NS', 'SANOFI.NS', 'GLAXO.NS', 'HFCL.NS', 'MSUMI.NS', 'BERGEPAINT.NS', 'GMDCLTD.NS', 'GESHIP.NS', 'ABSLAMC.NS', 'NBCC.NS', 'SAREGAMA.NS', 'RBLBANK.NS', 'LAURUSLABS.NS', 'JKLAKSHMI.NS', 'HONASA.NS',
                    'NAVINFLUOR.NS', 'TTML.NS', 'CLEAN.NS', 'CHEMPLASTS.NS', 'GUJGASLTD.NS', 'SAMMAANCAP.NS', 'DBREALTY.NS', 'GRANULES.NS', 'FINPIPE.NS', 'CROMPTON.NS', 'PNBHOUSING.NS', 'JYOTHYLAB.NS', 'KEI.NS', 'RAJESHEXPO.NS', 'DALBHARAT.NS', 'KIMS.NS', 'APTUS.NS', 'SAPPHIRE.NS', 'VIPIND.NS', 'WELCORP.NS', 'NUVOCO.NS', 'CUB.NS', 'GPPL.NS', 'KANSAINER.NS', 'NUVAMA.NS', 'AVANTIFEED.NS', 'GSPL.NS',
                    'RCF.NS', 'DEEPAKNTR.NS', 'JPPOWER.NS', 'LEMONTREE.NS', 'COROMANDEL.NS', 'AADHARHFC.NS', 'SWANENERGY.NS', 'GRINDWELL.NS', 'JBMA.NS', 'SCHAEFFLER.NS', 'J&KBANK.NS', 'JKCEMENT.NS', 'NH.NS', 'TANLA.NS', 'SUNDRMFAST.NS', 'PRAJIND.NS', 'DEEPAKFERT.NS', 'FLUOROCHEM.NS', 'NCC.NS', 'ASTERDM.NS', 'JWL.NS', 'SOBHA.NS', 'KAYNES.NS', 'PPLPHARMA.NS', 'RAMCOCEM.NS', 'VARROC.NS', 'GODREJIND.NS',
                    'KIRLOSENG.NS', 'CENTURYPLY.NS', 'FINCABLES.NS', 'ZEEL.NS', 'FORTIS.NS', 'CGCL.NS', 'GAEL.NS', 'CREDITACC.NS', 'GILLETTE.NS', 'BLUEDART.NS', 'SBFC.NS', 'EQUITASBNK.NS', 'CIEINDIA.NS', 'NETWORK18.NS', 'MAPMYINDIA.NS', 'ARE&M.NS', 'AARTIIND.NS', 'AWL.NS', 'GRINFRA.NS', 'ECLERX.NS', 'NAM-INDIA.NS', 'HOMEFIRST.NS', 'REDINGTON.NS', 'RHIM.NS', 'CYIENT.NS', 'HBLENGINE.NS', 'MAHSEAMLES.NS',
                    'CHOLAHLDNG.NS', 'UBL.NS', 'ENGINERSIN.NS', 'LTTS.NS', 'TBOTEK.NS']
def get_one_month_return(symbol):
    stock = yf.Ticker(symbol)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    price_data = stock.history(start=start_date, end=end_date)
    if price_data.empty:
        return None
    
    first_price = price_data['Close'].iloc[0]
    last_price = price_data['Close'].iloc[-1]
    
    return ((last_price - first_price) / first_price) * 100

# Function to fetch stock data
def get_stock_data(symbol, ma_days, ma_weights, nifty_return):
    stock = yf.Ticker(symbol)
    try:
        ist = pytz.timezone('Asia/Kolkata')
        end_date = datetime.now(ist)
        start_date = end_date - timedelta(days=400)  # Get more than 1 year of data for rolling windows
        price_data = stock.history(start=start_date, end=end_date)

        if price_data.empty:
            return None, None

        # Calculate moving averages dynamically based on user input
        ma_columns = {}
        for days in ma_days:
            column_name = f"{days} Day MA"
            price_data[column_name] = price_data['Close'].rolling(window=days).mean()
            ma_columns[column_name] = price_data[column_name].iloc[-1]

        latest_data = price_data.iloc[-1]
        current_price = latest_data['Close']

        # Determine highest order of MA broken and trend direction
        highest_ma_broken = 'None'
        trend = "Neutral"  # Default to neutral trend
        trend_color = "#d3d3d3"

        ma_comparison = {
            ma_name: ("Above" if current_price > ma_value else "Below")
            for ma_name, ma_value in ma_columns.items()
        }

        # Trend Analysis Using Recent 5-Day Price Movement
        last_3_prices = price_data['Close'].iloc[-3:].values
        three_day_avg = last_3_prices.mean()
        trend = "Neutral"
        trend_color = "gray"

        if last_3_prices[-1] > three_day_avg:  # Uptrend in last 5 days
            trend = "Uptrend"
            trend_color = "#abf7b1"
        elif last_3_prices[-1] < three_day_avg:  # Downtrend in last 5 days
            trend = "Downtrend"
            trend_color = "#FF9A98"
        # Scoring system: +100 to -100
        score = 0  # Start with neutral score
        for ma_name, weight in ma_weights.items():
            if ma_comparison.get(ma_name) == "Above":
                if trend == "Uptrend":
                    score += weight
            elif ma_comparison.get(ma_name) == "Below":
                if trend == "Downtrend":
                    score -= weight

        # Detect Moving Average Crossovers
        ma_crossovers = {}
        for i in range(len(ma_days) - 1):
            short_ma = f"{ma_days[i]} Day MA"
            long_ma = f"{ma_days[i+1]} Day MA"

            if short_ma in ma_columns and long_ma in ma_columns:
                # Check if short MA is now above long MA but was below in the previous period
                if len(price_data) < 2:
                    ma_crossovers[f"{short_ma} crossing {long_ma}"] = "No"
                    continue

            previous_short_ma = price_data[short_ma].iloc[-2] if not pd.isna(price_data[short_ma].iloc[-2]) else None
            previous_long_ma = price_data[long_ma].iloc[-2] if not pd.isna(price_data[long_ma].iloc[-2]) else None

            current_short_ma =  price_data[short_ma].iloc[-1] if not pd.isna(price_data[short_ma].iloc[-1]) else None 
            current_long_ma = price_data[long_ma].iloc[-1] if not pd.isna(price_data[long_ma].iloc[-1]) else None  # Most recent MA

            if previous_short_ma is not None and previous_long_ma is not None:
                # Bearish Crossover (Death Cross)
                if previous_short_ma > previous_long_ma and current_short_ma < current_long_ma:
                    ma_crossovers[f"{short_ma} crossing {long_ma}"] = "Yes"
                    trend_color = "#B47EE5"
                # Bullish Crossover (Golden Cross)
                elif previous_short_ma < previous_long_ma and current_short_ma > current_long_ma:
                    ma_crossovers[f"{short_ma} crossing {long_ma}"] = "Yes"
                    trend_color = "yellow"
                else:
                    ma_crossovers[f"{short_ma} crossing {long_ma}"] = "No"
                 
        # Calculate 1-month relative strength vs NIFTY
        stock_return = get_one_month_return(symbol)
        relative_strength = (stock_return - nifty_return) if stock_return is not None else None
        result_data = {
            'Symbol': symbol.removesuffix(".NS"),
            'Latest Price': current_price,
            #'Above/Below All': above_below,
            'Score': score,
            'Trend': trend,
            'Relative Strength vs NIFTY (%)': f"{relative_strength:.2f}" if relative_strength is not None else "N/A",
            '_trend_color': trend_color  # Keep as last column
        }
        result_data.update(ma_comparison) 
        result_data.update(ma_crossovers)  # Add MA crossovers

        return price_data, result_data
    except Exception as e:
        st.error(f"Error processing symbol {symbol}: {e}")
        return None, None

# Function to fetch fundamental data
def get_fundamental_data(symbol):
    stock = Ticker(symbol)
    try:
        info = yf.Ticker(symbol).info
        key_stats = stock.key_stats[symbol]
        financials = stock.financial_data[symbol]
        income_statement = stock.income_statement(frequency="a")

        # Extract fundamental metrics
        eps = key_stats.get("trailingEps", "N/A")
        pe_ratio = info.get("trailingPE", "N/A")
        if pe_ratio != "N/A":
            pe_ratio = round(float(pe_ratio),2)
        sector = info.get("sector", "N/A")
        market_cap = info.get('marketCap' , 'N/A') // 10000000
        revenue_growth = financials.get("revenueGrowth", "N/A")
        fii_dii_holding = key_stats.get("heldPercentInstitutions", "N/A")

        # Get revenue growth manually if not available
        if revenue_growth == "N/A" and not income_statement.empty:
            sorted_revenue = income_statement.sort_values(by="asOfDate", ascending=False)
            if len(sorted_revenue) > 1:
                latest_revenue = sorted_revenue.iloc[0]["TotalRevenue"]
                previous_revenue = sorted_revenue.iloc[1]["TotalRevenue"]
                revenue_growth = ((latest_revenue - previous_revenue) / previous_revenue) * 100

        return {
            "Earnings Per Share (EPS)": eps,
            "P/E Ratio": pe_ratio,
            "Revenue Growth (YoY)": f"{revenue_growth:.2f}%" if revenue_growth != "N/A" else "N/A",
            "Institutional Holdings (FII/DII %)": f"{fii_dii_holding * 100:.2f}%" if fii_dii_holding != "N/A" else "N/A",
            "Sector": sector,
            "Market Cap in Cr.": market_cap
        }
    except Exception as e:
        st.error(f"Error fetching fundamentals for {symbol}: {e}")
        return None

# Streamlit app
def main():
    st.title("Stock Moving Average Breakout Analysis")

    st.sidebar.subheader("Stock Selection")
    selection_option = st.sidebar.selectbox("Select Stock Category", ["Upload CSV / Manual Entry", "NIFTY Top 50", "NIFTY NEXT 150", "NIFTY NEXT 300"])
    
    # Reset session state when selection changes
    if "previous_selection" not in st.session_state or st.session_state["previous_selection"] != selection_option:
        st.session_state.clear()
        st.session_state["previous_selection"] = selection_option  # Store selection

    symbols = []
    
    if selection_option == "Upload CSV / Manual Entry":
        # Sidebar input
        uploaded_file = st.sidebar.file_uploader("Upload CSV with a single 'symbol' column without empty rows.", type="csv")

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            if 'symbol' not in df.columns:
                st.error("Uploaded CSV must have a 'symbol' column.")
                return
            symbols = [symbol.strip().upper() + '.NS' for symbol in df['symbol']]

            #Reset session state to ensure new data is processed
            if "uploaded_symbols" not in st.session_state or st.session_state["uploaded_symbols"] != symbols:
                st.session_state.clear()  # Reset session state if new file is uploaded
                st.session_state["uploaded_symbols"] = symbols  # Store uploaded symbols
        
        else:
            symbols_input = st.sidebar.text_input("Enter stock symbols (comma-separated)", value="SBIN,PHARMABEES,ULTRACEMCO,AXISBANK,BHARTIARTL,ZOMATO,PAYTM,OFSS,INDIGO,HAL,PERSISTENT,POLYCAB,BSE,MTNL,CDSL,NUVAMA,APARINDS,TECHNOE,TRIVENI,360ONE,JYOTISTRUC,CONCORDBIO,ZENTEC,GOLDIAM,GRAVITA,NEWGEN,ZAGGLE,ANGELONE,IRFC,IRCON,NMDC,TCS,LT")
            symbols = [symbol.strip().upper() + '.NS' for symbol in symbols_input.split(',')]

    elif selection_option == "NIFTY Top 50":
        symbols = NIFTY_TOP_50
    elif selection_option == "NIFTY NEXT 150":
        symbols = NIFTY_NEXT_150
    elif selection_option == "NIFTY NEXT 300":
        symbols = NIFTY_NEXT_300


    # Moving averages selection
    st.sidebar.subheader("Moving Averages Settings")
    ma_days = st.sidebar.text_input("Enter MA Days (comma-separated, e.g., 200,50,20)", value="200,50,20")
    ma_days = sorted([int(x.strip()) for x in ma_days.split(',') if x.strip().isdigit()], reverse=True)

    nifty_return = get_one_month_return("^NSEI")
    # Scoring weights
    st.sidebar.subheader("Scoring Weights")
    default_weights = [50, 30, 20]  # Default weights for top 3 MAs
    ma_weights = {}
    for i, days in enumerate(ma_days):
        default_value = default_weights[i] if i < len(default_weights) else 10
        ma_weights[f"{days} Day MA"] = st.sidebar.number_input(f"{days} Day MA Weight", min_value=0, max_value=100, value=default_value)

    if "technical_data" not in st.session_state or st.session_state["uploaded_symbols"] != symbols:
        results = []
        for symbol in symbols:
            _, result = get_stock_data(symbol, ma_days, ma_weights, nifty_return)
            if result:
                results.append(result)

        if results:
            st.session_state["technical_data"] = results
            st.session_state["uploaded_symbols"] = symbols

    else:
        results = st.session_state["technical_data"]
    # Display results
    if results:
        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values(by='Score' , key=abs, ascending=False).reset_index(drop=True)
        st.subheader("Stock Signals")

        # Extract trend colors before dropping the column
        trend_colors = results_df['_trend_color']
        
        # Remove the internal color column
        results_df = results_df.drop('_trend_color' , axis=1)

        # Modified highlight function to use the stored colors
        def highlight_trend(row):
            color = trend_colors[row.name]
            return [f'background-color: {color}' for _ in row]

        styled_df = results_df.style.apply(highlight_trend, axis=1)
        selected_row = st.dataframe(styled_df, use_container_width=True)
        st.subheader("Stock Signals")
        # Get fundamentals for the selected stock on hover/click
        selected_stock = st.selectbox("Select a stock to view fundamentals", results_df['Symbol'].tolist())

        if selected_stock:
            stock_symbol = selected_stock + ".NS"
            if "fundamental_data" not in st.session_state or st.session_state["last_selected"] != stock_symbol:
                st.session_state["fundamental_data"] = get_fundamental_data(stock_symbol)
                st.session_state["last_selected"] = stock_symbol

            fundamentals = st.session_state["fundamental_data"]

            if fundamentals:
                st.subheader(f"Fundamental Data for {selected_stock}")

                # Display key fundamental metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("Earnings Per Share (EPS)", fundamentals["Earnings Per Share (EPS)"])
                col2.metric("P/E Ratio", fundamentals["P/E Ratio"])
                col3.metric("Market Cap in Cr.", fundamentals["Market Cap in Cr."])

                col4, col5= st.columns(2)
                col4.metric("Revenue Growth (YoY)", fundamentals["Revenue Growth (YoY)"])
                col5.metric("Institutional Holdings (FII/DII %)", fundamentals["Institutional Holdings (FII/DII %)"])
                #col6.metric("Sector", fundamentals["Sector"])
                                # Display Sector with smaller font using markdown & CSS
                st.markdown(
                    f"""
                    <div style="text-align: center; font-size:16px; font-weight:bold; background-color:#f0f0f0; padding:8px; border-radius:5px; display:inline-block;">
                        Sector: {fundamentals["Sector"]}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

if __name__ == "__main__":
    main()
