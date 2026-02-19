from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

PRODUCTS = [
    {"id": 1,  "name": "Headphones",   "price": 89.99,  "emoji": "🎧"},
    {"id": 2,  "name": "Sneakers",     "price": 64.99,  "emoji": "👟"},
    {"id": 3,  "name": "Smart Watch",  "price": 139.99, "emoji": "⌚"},
    {"id": 4,  "name": "Backpack",     "price": 94.99,  "emoji": "🎒"},
    {"id": 5,  "name": "Sunglasses",   "price": 39.99,  "emoji": "🕶️"},
    {"id": 6,  "name": "Coffee Maker", "price": 54.99,  "emoji": "☕"},
    {"id": 7,  "name": "Yoga Mat",     "price": 32.99,  "emoji": "🧘"},
    {"id": 8,  "name": "Desk Lamp",    "price": 44.99,  "emoji": "💡"},
    {"id": 9,  "name": "Keyboard",     "price": 109.99, "emoji": "⌨️"},
    {"id": 10, "name": "Water Bottle", "price": 27.99,  "emoji": "🍶"},
]

@app.route("/")
def index():
    return render_template("index.html", products=PRODUCTS)

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
