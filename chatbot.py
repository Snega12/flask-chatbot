from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Enable Debug Mode
app.config['DEBUG'] = True  

# WooCommerce API Credentials
WC_API_URL = "https://heicecreams.com/wp-json/wc/v3"
CONSUMER_KEY = "ck_2acfbf02f0148f0a97ce5501031c41fd68d3c598"
CONSUMER_SECRET = "cs_1dec05cd51e244b7182c8f1feeb96db3a549c170"

# Handle favicon.ico request to avoid 404 errors
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, ''), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Home Route
@app.route('/')
def home():
    return "Chatbot is running!"

# Chatbot Logic
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '').lower()

    if "menu" in user_input or "flavors" in user_input:
        return jsonify({"reply": "We have Vanilla, Chocolate, Strawberry, and Mango flavors. What would you like?"})

    elif "order" in user_input:
        return jsonify({"reply": "Great! You can place an order at https://heicecreams.com/shop or tell me what you want."})

    elif "price" in user_input:
        return jsonify({"reply": "Our ice creams start at $5 per scoop. Would you like to order now?"})

    elif "available" in user_input:
        products = get_available_products()
        return jsonify({"reply": f"We currently have: {', '.join(products)}."})

    else:
        return jsonify({"reply": "Sorry, I didn't understand that. You can ask about flavors, price, or how to order."})

# Function to Get Products from WooCommerce API
def get_available_products():
    try:
        response = requests.get(f"{WC_API_URL}/products", auth=(CONSUMER_KEY, CONSUMER_SECRET))
        products = response.json()
        return [product['name'] for product in products] if isinstance(products, list) else ["Error fetching products"]
    except Exception as e:
        return [f"Error: {str(e)}"]

# Run Flask App in Debug Mode
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
