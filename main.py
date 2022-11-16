import yfinance as yf
import yahoo_fin.stock_info as si
import datetime
import streamlit as st
import pandas as pd
import numpy as np

def main():

    header = st.container()
    UserInput = st.container()
    dataset = st.container()
    results = st.container()

    
    #Test sürümü için stok listesi
    stockDict = {"Amazon":"AMZN", "Apple" : "AAPL", "Cisco":"CSCO", "Google":"GOOGL", "IBM": "IBM", "Intel": "INTC", "Microsoft":"MSFT", "Oracle":"ORCL", "Snowflake":"SNOW", "Twilio":"TWLO"}

    with header:
        st.title("Beta Calculation Program")

    with UserInput:
        st.header("Please Provide Information Needed")
        st.markdown("Choose a stock and date range, please")

        firstCol, secCol = st.columns(2)
        # Requires user selection from the stock list
        choosenStock = firstCol.selectbox("Stock", options=stockDict.keys())
        # Displays ticker name of the selected stock
        choosenTicker = stockDict[choosenStock]
        # Calender components for user's date entry
        startDate = firstCol.date_input("Pick a start date ", max_value= datetime.datetime.now ())
        secCol._text_input("Ticker", choosenTicker, disabled=True)
        endDate = secCol.date_input("Pick an end date", min_value= startDate, max_value= datetime.datetime.now ())

    with dataset:
        st.header("Historical Data")
        st.text("Historical data is feed via by Yahoo Finance")
        # Calculates daily return of the selected stock share
        dfs = si.get_data(choosenTicker, start_date = startDate, end_date = endDate)
        dfs["daily return"] = dfs["adjclose"].pct_change()
        dfs["daily return"] = dfs["daily return"]*100
        # Calculates daily return of the market index
        dfm = si.get_data("NDX", start_date = startDate, end_date = endDate)
        dfm["daily return"] = dfm["adjclose"].pct_change()
        dfm["daily return"] = dfm["daily return"]*100
        st.subheader(f"{choosenStock} historical data")
        st.write(dfs.head())
        st.subheader(f"Market historical data")
        st.write(dfm.head())

    with results:
        # Checks for compatibility of data in regard of dataframe length
        if dfs.shape[0] == dfm.shape[0]:
            index = list(range(dfs.shape[0]))
            n = dfs.shape[0] - 1
            # Defines the table of Decomposition of Returns for the Single-Index Model
            returnsTable = {'Index': index, 'Return on Stock': dfs["daily return"], 'Return on Market': dfm["daily return"]}
            returnsTableDf = pd.DataFrame(data=returnsTable)
            # save button ile kullanıcıya kaydetme imkanı verilmeli. returnsTableDf.to_csv(path)
            st.header("Decomposition of Returns")
            st.write(returnsTableDf)

            # Calculation of the Variance of the Return on Market and Return on Stock
            meanReturnMarket = np.mean(returnsTableDf["Return on Market"][1:])
            meanReturnStock = np.mean(returnsTableDf["Return on Stock"][1:])
            # Defines the variable for the sum of Return on Market minus Mean
            sumVarMarket = 0
            # Defines the variable of the product of the Return on Market minus Mean and Return on Stock minus Mean
            sumProduct = 0
            i = 1
            while i <=n:
                sumVarMarket += np.square(returnsTableDf.iloc[i][2] - meanReturnMarket)
                sumProduct += (returnsTableDf.iloc[i][1] - meanReturnStock)*(returnsTableDf.iloc[i][2] - meanReturnMarket)
                i +=1

            varReturnMarket = sumVarMarket/n         # the Variance of the Return on Market
            covarReturnStock = sumProduct/n
            beta = covarReturnStock / varReturnMarket
            alpha = meanReturnStock - meanReturnMarket*beta
            st.header("Results")
            st.write(f"* **the Variance of the Return on Market**: {varReturnMarket:.3f}")
            st.write(f"* the Variance of the Return on Stock has been calculated as {covarReturnStock:.3f}")
            st.write(f"* the beta has been calculated: {beta:.3f}")

        pd.DataFrame()

if __name__ == '__main__':
    main()