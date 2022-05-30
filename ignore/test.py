import yfinance as yf

df = yf.download(tickers= 'BTC-USD',start ='2022-05-01', interval='1h')
print(df)
