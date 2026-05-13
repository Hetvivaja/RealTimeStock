import dash
from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc
from graph.stock import generate_plotly_chart, get_stock_data
import plotly.graph_objs as go

def init_dash(server):
    dash_app = dash.Dash(
        __name__,
        server=server,
        routes_pathname_prefix='/dash/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    dash_app.layout = dbc.Container([
        html.H2("Stock Chart Viewer", className="text-center my-3"),
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='symbol-store', data=''),
        dcc.Dropdown(
            id='chart-type',
            options=[{'label': c, 'value': c} for c in ['Line', 'Bar', 'Candle', 'Area']],
            value='Line',
            className='my-2',
            style={'fontSize':20}
        ),
        dcc.RadioItems(
            id='period',
            options=[{'label': p, 'value': p} for p in ['1d', '5d', '1mo', '3mo', '6mo', '1y']],
            value='1mo',
            className='mb-3',style={'display':'flex','fontSize':20},labelStyle={'margin-right': '20px'},
        ),
        dcc.Graph(id='stock-chart'),
        html.Div(id='stock-info'),
    ])

    @dash_app.callback(
        Output('symbol-store', 'data'),
        [Input('url', 'pathname')]
    )
    def update_symbol_store_from_url(pathname):
        if pathname and pathname.startswith('/dash/stock/'):
            return pathname.split('/')[-1].upper()
        return ""

    @dash_app.callback(
        [Output('stock-chart', 'figure'), Output('stock-info', 'children')],
        [Input('symbol-store', 'data'), Input('chart-type', 'value'), Input('period', 'value')]
    )
    def update_chart(symbol, chart_type, period):
        if not symbol:
            return go.Figure(), ""

        figure = generate_plotly_chart(symbol.upper(), chart_type, period)
        info = get_stock_data(symbol.upper())

        has_chart = bool(figure.data)

        if not has_chart and not info:
            return go.Figure(), html.P("No data available for this stock or period.")
        if not has_chart:
            return go.Figure(), info_card_from_info(info, symbol) if info else html.P("Chart data not available.")
        if not info:
            return figure, html.P("Stock information not available.")

        return figure, info_card_from_info(info, symbol)

    def info_card_from_info(info, symbol):
        if not info:
            return html.P("No stock information available.")
        return html.Div([
            html.H4(f"{info.get('name', 'N/A')} ({symbol.upper()})"),
            html.P(f"Open: {info.get('open', 'N/A')}"),
            html.P(f"Close: {info.get('close', 'N/A')}"),
            html.P(f"Volume: {info.get('volume', 'N/A')}"),
            html.P(f"Market Cap: {info.get('marketCap', 'N/A')}"),
            html.P(f"Beta: {info.get('beta', 'N/A')}"),
            html.P(f"PE Ratio: {info.get('peRatio', 'N/A')}"),
            html.P(f"EPS: {info.get('eps', 'N/A')}"),
            html.P(f"Earnings Date: {info.get('earningsDate', 'N/A')}"),
            html.P(f"Bid: {info.get('bid', 'N/A')}"),
            html.P(f"Ask: {info.get('ask', 'N/A')}"),
            html.P(f"Day Range: {info.get('dayRange', ['N/A', 'N/A'])[0]} - {info.get('dayRange', ['N/A', 'N/A'])[1]}"),
            html.P(f"52 Week Range: {info.get('fiftyTwoWkRange', ['N/A', 'N/A'])[0]} - {info.get('fiftyTwoWkRange', ['N/A', 'N/A'])[1]}"),
            html.P(f"Average Volume: {info.get('avgVolume', 'N/A')}"),
            html.P(f"Target Price: {info.get('targetPrice', 'N/A')}")
        ], style={
            'border': '1px solid #ccc',
            'padding': '15px',
            'borderRadius': '8px',
            'marginBottom': '20px',
            'backgroundColor': '#f8f9fa',
            'fontSize':30
        })

    return dash_app
