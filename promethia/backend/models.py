from pydantic import BaseModel
from datetime import datetime
import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as ta
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
#from sklearn.metrics import classification_report

class StockQuery(BaseModel):
    ticker: str
    query_type: str
    timestamp: datetime


ticker = yf.Ticker("AAPL")
df = ticker.history(period="6mo")

df['MA_5'] = df['Close'].rolling(window=5).mean()
df['MA_20'] = df['Close'].rolling(window=20).mean()
df['RSI'] = ta.rsi(df['Close'], length=14)
df['MACD'] = ta.macd(df['Close'])['MACD_12_26_9']
df['Volatility'] = df['Close'].pct_change().rolling(window=14).std()
df['Slope'] = df['Close'].rolling(window=5).apply(lambda x: np.polyfit(range(5), x, 1)[0])

df.dropna(inplace=True)

def label_trend(row):
    if row['MA_5'] > row['MA_20'] and row['RSI'] > 55 and row['MACD'] > 0 and row['Slope'] > 0:
        return 'Uptrend'
    elif row['MA_5'] < row['MA_20'] and row['RSI'] < 45 and row['MACD'] < 0 and row['Slope'] < 0:
        return 'Downtrend'
    else:
        return 'Sideways'

df['Trend'] = df.apply(label_trend, axis=1)


features = ['MA_5', 'MA_20', 'RSI', 'MACD', 'Volatility', 'Slope']
X = df[features]
y = df['Trend']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)