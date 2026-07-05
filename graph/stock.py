import yfinance as yf
import plotly.graph_objs as go


def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return {
            'symbol': symbol,
            'name': info.get("shortName", "N/A"),
            'open': info.get("open", "N/A"),
            'close': info.get("previousClose", "N/A"),
            'volume': info.get("volume", "N/A"),
            'marketCap': info.get("marketCap", "N/A"),
            'beta': info.get("beta", "N/A"),
            'peRatio': info.get("trailingPE", "N/A"),
            'eps': info.get("trailingEps", "N/A"),
            'earningsDate': info.get("earningsDate", "N/A"),
            'bid': info.get("bid", "N/A"),
            'ask': info.get("ask", "N/A"),
            'dayRange': (
                info.get("dayLow", "N/A"),
                info.get("dayHigh", "N/A")
            ),
            'fiftyTwoWkRange': (
                info.get("fiftyTwoWeekLow", "N/A"),
                info.get("fiftyTwoWeekHigh", "N/A")
            ),
            'avgVolume': info.get("averageVolume", "N/A"),
            'targetPrice': info.get("targetMeanPrice", "N/A")
        }
    except Exception as e:
        print("Error getting stock data:", e)
        return None


def generate_plotly_chart(symbol, chart_type='Line', period='1mo'):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period=period)
    except Exception as e:
        print("Error getting chart data:", e)
        return go.Figure()

    if data.empty:
        return go.Figure()

    fig = go.Figure()
    if chart_type == 'Line':
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close'))
    elif chart_type == 'Bar':
        fig.add_trace(go.Bar(x=data.index, y=data['Close'], name='Close'))
    elif chart_type == 'Candle':
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']
        )])
    elif chart_type == 'Area':
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], fill='tozeroy', name='Close'))

    fig.update_layout(
        title=f"{symbol} - {chart_type} Chart",
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_white',
        margin=dict(l=42, r=24, t=72, b=42),
        font=dict(family='Segoe UI, Arial, sans-serif', color='#14213d'),
        hovermode='x unified',
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    return fig
