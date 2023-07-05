from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

# List of quotes
quotes = [
    "Quote 1",
    "Quote 2",
    "Quote 3",
    "Quote 4",
    "Quote 5"
]

@app.route('/')
def get_random_quote():
    random_quote = random.choice(quotes)
    return render_template('index.html', quote=random_quote)

if __name__ == '__main__':
    app.run(debug=True)
