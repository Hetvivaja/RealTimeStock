# import dash
# from dash import dcc, html, Input, Output
# import dash_bootstrap_components as dbc
# from graph.stock import generate_plotly_chart, get_stock_data
# import plotly.graph_objs as go

# def init_dash(server):
#     dash_app = dash.Dash(
#         __name__,
#         server=server,
#         routes_pathname_prefix='/dash/',
#         external_stylesheets=[dbc.themes.BOOTSTRAP]
#     )

#     dash_app.layout = dbc.Container([
#         html.H2("Stock Chart Viewer", className="text-center my-3"),
#         # dcc.Input(id='symbol-input', type='text', placeholder='Enter Stock Symbol', debounce=True),
#         dcc.Dropdown(
#             id='chart-type',
#             options=[{'label': c, 'value': c} for c in ['Line', 'Bar', 'Candle', 'Area']],
#             value='Line',
#             className='my-2'
#         ),
#         dcc.Dropdown(
#             id='period',
#             options=[{'label': p, 'value': p} for p in ['1d', '5d', '1mo', '3mo', '6mo', '1y']],
#             value='1mo',
#             className='mb-3'
#         ),
#         dcc.Graph(id='stock-chart'),
#         html.Div(id='stock-info'),
#     ])

#     @dash_app.callback(
#         [Output('stock-chart', 'figure'), Output('stock-info', 'children')],
#         [Input('symbol-input', 'value'), Input('chart-type', 'value'), Input('period', 'value'), Input('url', 'pathname')]
#     )
#     def update_chart(symbol, chart_type, period):
#         if not symbol:
#             return go.Figure(), ""
#         figure = generate_plotly_chart(symbol.upper(), chart_type, period)
#         info = get_stock_data(symbol.upper())
#         if not info:
#             return go.Figure(), html.P("No data available.")

#         info_card = html.Div([
#             html.H4(f"{info['name']} ({symbol.upper()})"),
#             html.P(f"Open: {info['open']}"),
#             html.P(f"Close: {info['close']}"),
#             html.P(f"Volume: {info['volume']}"),
#             html.P(f"Market Cap: {info['marketCap']}"),
#             html.P(f"Beta: {info['beta']}"),
#             html.P(f"PE Ratio: {info['peRatio']}"),
#             html.P(f"EPS: {info['eps']}"),
#             html.P(f"Earnings Date: {info['earningsDate']}"),
#             html.P(f"Bid: {info['bid']}"),
#             html.P(f"Ask: {info['ask']}"),
#             html.P(f"Day Range: {info['dayRange'][0]} - {info['dayRange'][1]}"),
#             html.P(f"52 Week Range: {info['fiftyTwoWkRange'][0]} - {info['fiftyTwoWkRange'][1]}"),
#             html.P(f"Average Volume: {info['avgVolume']}"),
#             html.P(f"Target Price: {info['targetPrice']}")
#         ], style={
#             'border': '1px solid #ccc',
#             'padding': '15px',
#             'borderRadius': '8px',
#             'marginBottom': '20px',
#             'backgroundColor': '#f8f9fa'
#         })

#         return figure, info_card
   
#     return dash_app
import dash
from dash import dcc, html, Input, Output, State # Import State as well
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
        

        # 1. Add dcc.Location to get the URL pathname
        dcc.Location(id='url', refresh=False),

        # 2. Add dcc.Store to hold the extracted stock symbol
        # This component will store the symbol (e.g., 'LMT', 'RBRK')
        # retrieved from the URL, making it available as an Input.
        dcc.Store(id='symbol-store', data=''), # Initialize with empty data

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

    # Callback to parse the URL and update the symbol-store
    @dash_app.callback(
        Output('symbol-store', 'data'),
        [Input('url', 'pathname')]
    )
    def update_symbol_store_from_url(pathname):
        if pathname and pathname.startswith('/dash/stock/'):
            # Assuming your URL format is /dash/stock/<SYMBOL>
            symbol = pathname.split('/')[-1].upper()
            return symbol
        return "" # Return empty if no valid symbol in URL

    @dash_app.callback(
        [Output('stock-chart', 'figure'), Output('stock-info', 'children')],
        # Change Input('symbol-input', 'value') to Input('symbol-store', 'data')
        [Input('symbol-store', 'data'), Input('chart-type', 'value'), Input('period', 'value')]
        # Removed Input('url', 'pathname') from here as it's now handled by update_symbol_store_from_url
    )
    def update_chart(symbol, chart_type, period):
        if not symbol:
            return go.Figure(), ""
        
        # Ensure generate_plotly_chart and get_stock_data handle potential errors
        figure = generate_plotly_chart(symbol.upper(), chart_type, period)
        info = get_stock_data(symbol.upper())

        if not figure and not info: # If both fail, indicate no data
            return go.Figure(), html.P("No data available for this stock or period.")
        elif not figure: # If only figure generation fails
            return go.Figure(), info_card_from_info(info, symbol) if info else html.P("Chart data not available.")
        elif not info: # If only info acquisition fails
            return figure, html.P("Stock information not available.")

        # Helper function to generate info card (optional, but keeps update_chart cleaner)
        info_card = info_card_from_info(info, symbol)

        return figure, info_card

    # Helper function to create the info card HTML
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