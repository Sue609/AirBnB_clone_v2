#!/usr/bin/python3

from flask import Flask

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Function that displays hello bnb
    """
    return "Hello HBNB!"

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Function that displays hbnb
    """
    return "hbnb"

@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """
    Function that displays C followed by text.
    """
    text = text.replace("_", " ")
    return f"C {text}"

@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_route(text='is cool'):
    """
    Function that displays python followed by text
    """
    return "Python {}".format(text.replace('_', ' '))

@app.route("/number/<int:n>")
    