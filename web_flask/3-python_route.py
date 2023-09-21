#!/usr/bin/python3
from flask import Flask

app = Flask(__name__)

@app.route("/", strict_slashes=False)
def hello_hbnb():
    """
    Script that displays hello hbnb.
    """
    return "Hello HBNB"

@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """
    Script that displays hbnb
    """
    return "HBNB"

@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """
    Function that displays C followed by text
    """
    text = text.replace("_", " ")
    return f"(C {text})"

@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_route(text="is cool"):
    """
    Funtion that displays python followed by text
    """
    return "Python {}".format(text.replace('_', ' '))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)