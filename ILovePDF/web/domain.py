from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

# List of quotes
quotes = [
    "Straight to the point, no time for hellos.",
    "Chat time is precious, skip the hellos.",
    "Greetings are nice, but let's dive into the chat.",
    "No time for hellos, let's get down to business.",
    "Skip the pleasantries, let's chat efficiently.",
    "In this chat, hellos can take a backseat.",
    "Save time, skip the hellos, and dive in.",
    "Hello? Let's cut to the chase and start the chat.",
    "Quick chats, no time for greetings.",
    "Efficiency is key, no time for hellos."
]

@app.route('/')
def get_random_quote():
    random_quote = random.choice(quotes)
    return render_template('index.html', quote=random_quote)

if __name__ == '__main__':
    app.run(debug=True)
