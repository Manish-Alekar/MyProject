import util
from datetime import datetime as dt, date
import pandas as pd
import requests
from nsepy import get_history as gh
import dateutil.relativedelta as dr
import numpy as np
import matplotlib.pyplot as plt
pd.set_option('display.width',1500)
pd.set_option('display.max_rows',150)
pd.set_option('display.max_columns',50)
tradingsymbol = input("Enter the stock symbol : ")
end = date.today()
start = end - dr.relativedelta(days=180)
data = gh(tradingsymbol,start,end)
df = pd.DataFrame(data)
df =df[['Symbol', 'Open', 'High', 'Low', 'Close']]

rsi_period = 14
change = df['Close'].diff()
gain = change.mask(change < 0, 0)
loss = change.mask(change > 0, 0)

average_gain = gain.ewm(com = rsi_period-1, min_periods=rsi_period).mean()
average_loss = loss.ewm(com = rsi_period-1, min_periods=rsi_period).mean()
rs = abs(average_gain/average_loss)
rsi = 100 - (100/(1+rs))
df['rsi'] = rsi

df['ema10'] = df['Close'].ewm(span = 10).mean()
df['ema20'] = df['Close'].ewm(span = 20).mean()

df['Signal'] = 0.0



df['Signal'] = np.where((df['ema10'] > df['ema20']), 1.0, 0.0)

df['Position'] = df['Signal'].diff()
print(df)


plt.figure(figsize = (20,10))
df['Close'].plot(color = 'k', label= 'Close')
df['ema10'].plot(color = 'r',label = 'EMA 10')
df['ema20'].plot(color = 'b', label = 'EMA 20')

plt.plot(df[df['Position'] == 1].index,
df['ema10'][df['Position'] == 1],
'^', markersize = 15, color = 'g', label = 'buy')

plt.plot(df[df['Position'] == -1].index,
df['ema10'][df['Position'] == -1],
'v', markersize = 15, color = 'r', label = 'sell')
plt.ylabel('Price in Rupees', fontsize = 15 )
plt.xlabel('Date', fontsize = 15 )
plt.title(tradingsymbol, fontsize = 20)



plt.legend()
plt.grid()
plt.show()



