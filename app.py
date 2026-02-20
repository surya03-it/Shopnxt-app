import os
import logging
from flask import Flask, render_template, jsonify

# Log to stdout so errors appear in CloudWatch
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "shopnxt-key-2025")

# FIX: emoji removed from Python source - causes UnicodeDecodeError in
#      gunicorn on python:3.12-slim which has no locale set by default.
#      Emoji are now safe HTML entities inside the Jinja2 template only.
PRODUCTS = [
    {"id": 1,  "name": "Headphones",   "price": 89.99,  "icon": "&#127911;"},
    {"id": 2,  "name": "Sneakers",     "price": 64.99,  "icon": "&#128095;"},
    {"id": 3,  "name": "Smart Watch",  "price": 139.99, "icon": "&#8987;"},
    {"id": 4,  "name": "Backpack",     "price": 94.99,  "icon": "&#127890;"},
    {"id": 5,  "name": "Sunglasses",   "price": 39.99,  "icon": "&#128083;"},
    {"id": 6,  "name": "Coffee Maker", "price": 54.99,  "icon": "&#9749;"},
    {"id": 7,  "name": "Yoga Mat",     "price": 32.99,  "icon": "&#129340;"},
    {"id": 8,  "name": "Desk Lamp",    "price": 44.99,  "icon": "&#128161;"},
    {"id": 9,  "name": "Keyboard",     "price": 109.99, "icon": "&#9000;"},
    {"id": 10, "name": "Water Bottle", "price": 27.99,  "icon": "&#127870;"},
]


@app.route("/")
def index():
    logger.info("GET / - rendering index page")
    return render_template("index.html", products=PRODUCTS)


@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "shopnxt"}), 200


@app.errorhandler(404)
def not_found(e):
    logger.warning(f"404: {e}")
    return render_template("index.html", products=PRODUCTS), 200


@app.errorhandler(500)
def server_error(e):
    logger.error(f"500: {e}")
    return "<h2>Something went wrong. Please try again.</h2>", 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting ShopNxt on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)

