from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Global data for demonstration
inventory = [
    {"id": 1, "name": "Apples", "quantity": 10, "price": 0.5},
    {"id": 2, "name": "Milk", "quantity": 5, "price": 1.5},
]

stocks = {
    "AAPL": 150.0,
    "GOOGL": 2800.0,
    "AMZN": 3400.0,
    "MSFT": 300.0
}

portfolio = {
    "balance": 10000.0,
    "holdings": {}
}

@app.route('/')
def home():
    return "Python Backend is Running!"

# --- Calculator ---
@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.json
    try:
        result = eval(data['expression'])
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# --- Stock Trading Simulator ---
@app.route('/stock')
def stock():
    return render_template('stock.html', stocks=stocks, portfolio=portfolio)

@app.route('/api/stock/buy', methods=['POST'])
def buy_stock():
    data = request.json
    symbol = data['symbol']
    qty = int(data['quantity'])
    price = stocks[symbol]
    cost = price * qty
    
    if portfolio['balance'] >= cost:
        portfolio['balance'] -= cost
        portfolio['holdings'][symbol] = portfolio['holdings'].get(symbol, 0) + qty
        return jsonify(portfolio)
    return jsonify({"error": "Insufficient balance"}), 400

# --- Grocery Inventory App ---
@app.route('/inventory')
def inventory_page():
    return render_template('inventory.html', inventory=inventory)

@app.route('/api/inventory/add', methods=['POST'])
def add_inventory():
    data = request.json
    new_item = {
        "id": len(inventory) + 1,
        "name": data['name'],
        "quantity": int(data['quantity']),
        "price": float(data['price'])
    }
    inventory.append(new_item)
    return jsonify(inventory)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
