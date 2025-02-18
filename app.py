from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import re

app = Flask(__name__)
socketio = SocketIO(app)

class IceCreamChatbot:
    def __init__(self):
        self.faqs = {
            'flavors': (
                "We offer a delightful range of flavors, including:\n"
                "- Vanilla\n"
                "- Chocolate\n"
                "- Strawberry\n"
                "- Mango\n"
                "- Black Forest\n"
                "- Roasted Almond\n"
                "- Lychee\n"
                "- Black Currant\n"
                "- Red Velvet\n"
                "- Pistachio etc.."
            ),
            'categories': (
                "We offer ice creams in the following categories:\n"
                "- **Classic**: Timeless favorites like Vanilla, Chocolate, and Strawberry.\n"
                "- **Exotic**: Unique flavors such as Lychee, Black Currant, and Red Velvet.\n"
                "- **Day-to-Day Purchasing**: Popular choices available for regular purchase.\n"
                "- **Raw Materials for Kitchen**: Ingredients for making your own ice cream or desserts.\n"
                "- **Cakes**: Delicious ice cream cakes for celebrations and special occasions."
            ),
            'raw materials': (
                "We provide high-quality raw materials for making ice creams and desserts, including:\n"
                "- Ice cream bases\n"
                "- Flavored syrups\n"
                "- Chocolate chips\n"
                "- Nuts and dry fruits\n"
                "- Whipping cream\n"
                "- Waffle cones and cups\n"
                "These ingredients are perfect for professional and home use!"
            ),
            'day to day purchasing': (
                "Yes! We offer convenient options for daily purchases. You can buy your favorite ice creams in:\n"
                "- Single scoops\n"
                "- Family packs\n"
                "- Take-home tubs\n"
                "- Party packs\n"
                "Order online or visit our store for quick and easy purchases!"
            ),
            'vegan': "Yes, we offer a selection of vegan ice creams made from plant-based ingredients.",
            'order': "You can place an order directly on our website by selecting your favorite ice cream and adding it to your cart.",
            'delivery': "Currently, we do not provide home delivery. **All products must be collected from the main branch** after placing an order.",
            'return': "We do not accept returns due to the perishable nature of our products, but feel free to contact us if there’s an issue with your order.",
            'customize': "Yes, you can customize your ice cream with toppings like nuts, fruits, and syrups at no extra cost!",
            'hours': "We are open from 10 AM to 10 PM every day of the week.",
            'price': "For pricing details, please visit our website: [heicecreams.com](https://www.heicecreams.com).",
            'bulk discount': "Yes, we offer discounts for bulk orders. Please contact us for more details."
        }
    
    def match_question(self, question):
        question = question.lower()
        for key in self.faqs:
            if re.search(key, question):
                return self.faqs[key]
        return None

    def get_answer(self, question):
        return self.match_question(question) or "Sorry, I don't have an answer to that question. Can I help with something else?"

# Create an instance of the chatbot
chatbot = IceCreamChatbot()

@app.route("/")
def index():
    return render_template("chatbot.html")

# WebSocket route for receiving and sending messages
@socketio.on('message')
def handle_message(user_message):
    bot_response = chatbot.get_answer(user_message)
    emit('response', bot_response)  # Send the bot response back to the client

if __name__ == "__main__":
    socketio.run(app, debug=True)
