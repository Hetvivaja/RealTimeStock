from flask import Flask, redirect, render_template, request, url_for
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
    return render_template('stock_data.html', symbol=symbol)

if __name__ == "__main__":
    app.run(debug=True)
