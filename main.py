from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import requests
import numpy as np
import tensorflow as tf
from datetime import datetime, timedelta
import os
import json

# Initialize the Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key"
app.config["JWT_SECRET_KEY"] = "your-jwt-secret-key"
jwt = JWTManager(app)

# Simulated user database
users = {"admin": {"password": "password"}}

# API keys and settings (Alpha Vantage key is fixed here)
ALPHA_VANTAGE_API_KEY = "N05VJZGC8YKVDPRP"
NEWS_API_KEY = "your_news_api_key"  # Replace with your News API key

# Routes for static React files
@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")

@app.route("/static/<path:path>")
def static_files(path):
    return send_from_directory("frontend/static", path)

# User authentication
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if username in users:
        return jsonify({"msg": "User already exists"}), 400
    users[username] = {"password": password}
    return jsonify({"msg": "User registered successfully"}), 200

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if username not in users or users[username]["password"] != password:
        return jsonify({"msg": "Invalid credentials"}), 401
    token = create_access_token(identity=username, expires_delta=timedelta(hours=1))
    return jsonify({"token": token}), 200

# Market data integration
@app.route("/api/market_data", methods=["GET"])
def market_data():
    symbol = request.args.get("symbol", "AAPL")
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    return jsonify(response.json())

# News sentiment analysis
@app.route("/api/news", methods=["GET"])
def news():
    query = request.args.get("query", "stocks")
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    news_data = response.json()
    # Simulate sentiment analysis
    sentiment_scores = [{"title": article["title"], "sentiment": np.random.choice(["Positive", "Negative", "Neutral"])} for article in news_data.get("articles", [])]
    return jsonify(sentiment_scores)

# Basic AI for algorithmic trading (mocked for simplicity)
@app.route("/api/ai_trade", methods=["POST"])
def ai_trade():
    data = request.json
    # Simulate AI-based trading decision
    decision = np.random.choice(["Buy", "Sell", "Hold"])
    return jsonify({"decision": decision})

# Backtesting
@app.route("/api/backtest", methods=["POST"])
def backtest():
    data = request.json
    symbol = data.get("symbol", "AAPL")
    # Mocked backtesting results
    return jsonify({"symbol": symbol, "profit": np.random.uniform(-1000, 1000)})

# Run the app
if __name__ == "__main__":
    if not os.path.exists("frontend"):
        os.makedirs("frontend/static")
        # Create a simple React app
        with open("frontend/index.html", "w") as f:
            f.write("""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Trading App</title>
                    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                </head>
                <body>
                    <h1>Trading App</h1>
                    <div id="app">Loading...</div>
                    <script>
                        // Simulated frontend logic
                        document.getElementById('app').innerHTML = '<h2>React App Coming Soon!</h2>';
                    </script>
                </body>
                </html>
            """)
    app.run(host="0.0.0.0", port=5000)
