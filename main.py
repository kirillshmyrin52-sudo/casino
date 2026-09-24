import os
from flask import Flask, jsonify, request, send_from_bytes
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Временная база данных в оперативной памяти, чтобы ничего не падало
users_db = {
    77665544: {"balance": 0.041, "inventory": []}
}

@app.route('/')
def home():
    return "🔥 Бэкенд Render успешно запущен и готов к работе!"

@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if user_id not in users_db:
        users_db[user_id] = {"balance": 0.041, "inventory": []}
    return jsonify(users_db[user_id])

@app.route('/api/bet', methods=['POST'])
def place_bet():
    data = request.json or {}
    user_id = data.get("user_id", 77665544)
    amount = float(data.get("bet_amount", 0.1))
    
    if user_id not in users_db:
        users_db[user_id] = {"balance": 0.041, "inventory": []}
        
    if users_db[user_id]["balance"] < amount:
        return jsonify({"status": "low_balance"}), 400
        
    users_db[user_id]["balance"] = round(users_db[user_id]["balance"] - amount, 3)
    return jsonify({"status": "success", "balance": users_db[user_id]["balance"]})

@app.route('/api/win', methods=['POST'])
def claim_win():
    data = request.json or {}
    user_id = data.get("user_id", 77665544)
    amount = float(data.get("amount", 0.0))
    
    if user_id not in users_db:
        users_db[user_id] = {"balance": 0.041, "inventory": []}
        
    users_db[user_id]["balance"] = round(users_db[user_id]["balance"] + amount, 3)
    return jsonify({"status": "success", "balance": users_db[user_id]["balance"]})

@app.route('/api/create-invoice', methods=['POST'])
def create_invoice():
    return jsonify({"link": ""})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
