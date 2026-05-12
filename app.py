from flask import Flask, render_template, request, redirect, url_for
from dash_app import init_dash
from graph.top import get_top

app = Flask(__name__)
init_dash(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    query = request.args.get('query')
    if query:
        return redirect(url_for('stock_detail', symbol=query.upper()))
    return redirect(url_for('home'))

@app.route('/top-stocks')
def top_stock():
    category = request.args.get('category', 'most_actives')
    top_symbols = get_top(screener_Id=category)
    return render_template('top_stock.html', symbols=top_symbols, selected_category=category)

@app.route('/stock/<symbol>')
def stock_detail(symbol):
    return render_template('stock_data.html', symbol=symbol)  # Just loads the Dash chart

if __name__ == "__main__":
    app.run(debug=True)


# from dash import Dash, html, dcc, Input, Output,dash
# from graph.stock import get_stock_chart
# import dash_bootstrap_components as dbc

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# app.title = "Stock Dashboard"

# app.layout = html.Div([
#     html.H2("Stock Dashboard"),

#     dcc.Input(id="stock-input", value="AAPL", type="text", debounce=True),
    
#     dcc.Dropdown(
#         id="chart-type",
#         options=['line', 'bar', 'area', 'candlestick'],
#         value='line',
#         clearable=False
#     ),

#     dcc.RadioItems(
#         id="duration",
#         options=["1d","5d","1mo","6mo","1y"],style={"display":"flex",'topMargin':10},
#         value="1mo",
#     ),

#     dcc.Graph(id="stock-chart")
# ])


# @app.callback(
#     Output("stock-chart", "figure"),
#     Input("stock-input", "value"),
#     Input("chart-type", "value"),
#     Input("duration", "value"),
# )
# def update_chart(symbol, chart_type, period):
#     return get_stock_chart(symbol.upper(), chart_type, period)

# if __name__ == "__main__":
#     app.run(debug=True)
