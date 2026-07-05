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
        html.Div([
            html.Div([
                html.P("Chart workspace", className="dash-eyebrow"),
                html.H2("Stock Chart Viewer"),
            ]),
        ], className="dash-title"),
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='symbol-store', data=''),
        html.Div([
            html.Label("Chart Type", htmlFor="chart-type"),
            dcc.Dropdown(
                id='chart-type',
                options=[{'label': c, 'value': c} for c in ['Line', 'Bar', 'Candle', 'Area']],
                value='Line',
                clearable=False,
            ),
            html.Label("Period", htmlFor="period"),
            dcc.RadioItems(
                id='period',
                options=[{'label': p, 'value': p} for p in ['1d', '5d', '1mo', '3mo', '6mo', '1y']],
                value='1mo',
                className='period-toggle',
                labelStyle={'margin': 0},
            ),
        ], className="dash-toolbar"),
        dcc.Graph(id='stock-chart'),
        html.Div(id='stock-info'),
    ], fluid=True, className="dash-shell")

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
            html.H3(f"{info.get('name', 'N/A')} ({symbol.upper()})", className="info-title"),
            html.Div([
                metric("Open", info.get('open', 'N/A')),
                metric("Previous Close", info.get('close', 'N/A')),
                metric("Volume", info.get('volume', 'N/A')),
                metric("Market Cap", info.get('marketCap', 'N/A')),
                metric("Beta", info.get('beta', 'N/A')),
                metric("PE Ratio", info.get('peRatio', 'N/A')),
                metric("EPS", info.get('eps', 'N/A')),
                metric("Earnings Date", info.get('earningsDate', 'N/A')),
                metric("Bid", info.get('bid', 'N/A')),
                metric("Ask", info.get('ask', 'N/A')),
                metric("Day Range", f"{info.get('dayRange', ['N/A', 'N/A'])[0]} - {info.get('dayRange', ['N/A', 'N/A'])[1]}"),
                metric("52 Week Range", f"{info.get('fiftyTwoWkRange', ['N/A', 'N/A'])[0]} - {info.get('fiftyTwoWkRange', ['N/A', 'N/A'])[1]}"),
                metric("Average Volume", info.get('avgVolume', 'N/A')),
                metric("Target Price", info.get('targetPrice', 'N/A')),
            ], className="info-grid")
        ], className="info-card")

    def metric(label, value):
        return html.Div([
            html.Span(label),
            html.Strong(str(value))
        ], className="metric")

    return dash_app
