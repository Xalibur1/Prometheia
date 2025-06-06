from models import model, df
import plotly.graph_objects as go

color_map = {
    'Uptrend': 'green',
    'Downtrend': 'red',
    'Sideways': 'gray'
}

fig = go.Figure(data=[
    go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='OHLC'
    ),
    go.Scatter(
        x=df.index,
        y=df['Close'],
        mode='markers',
        marker=dict(
            color=df['Trend'].map(color_map),
            size=7,
            opacity=0.8
        ),
        name='Trend',
        text=df['Trend'],
        hoverinfo='text+y'
    )
])

fig.update_layout(
    title='Stock Trend Classification - AAPL',
    xaxis_title='Date',
    yaxis_title='Price',
    xaxis_rangeslider_visible=False,
    template='plotly_white'
)
