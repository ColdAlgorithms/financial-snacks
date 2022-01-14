# import libraries
import yahoo_fin.stock_info as si
import pandas_datareader.data as data
import pandas as pd

#Dow Stock List
tickers= si.tickers_dow()


index = []
price = []
B = []
PE = []
EPS = []
market_cap = []
ev = []  #Enterprise Value = ( Market capitalization + total debt−cash and cash equivalents ) / EBITDA

for ticker in tickers:
    
    quote_table = si.get_quote_table(ticker)
    quote_yahoo = data.get_quote_yahoo(ticker)
    income_statement = si.get_income_statement(ticker)
    balance_sheet = si.get_balance_sheet(ticker)
    
    PE.append(quote_table["PE Ratio (TTM)"])
    EPS.append(quote_table["EPS (TTM)"])
    
    index.append(data.get_quote_yahoo(ticker)['shortName'])
    price.append(data.get_quote_yahoo(ticker)['price'])
    market_cap.append(data.get_quote_yahoo(ticker)['marketCap'])
    
    #book_value = data.get_quote_yahoo(ticker)['bookValue']
    
    #Enterprise Value = ( Market capitalization + total debt−cash and cash equivalents ) / EBITDA
    ev.append((data.get_quote_yahoo(ticker)['marketCap'] + balance_sheet.loc["totalLiab"][0]- balance_sheet.loc["cash"][0])/income_statement.loc["ebit"][0])
    print(balance_sheet.loc["totalLiab"])
    B.append(quote_table["Beta (5Y Monthly)"])
    
stocks_dict = {'Index': index, 'Prices': price, 'Beta': B, 'PE': PE, 'EPS': EPS, 'Enterprise Value': ev}
stocks = pd.DataFrame(data=stocks_dict)
stocks_csv = pd.DataFrame.to_csv(stocks)
print(stocks)
