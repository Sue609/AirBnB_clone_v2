#!/usr/bin/python3
"""
This module introduces a new function number_route.
"""

from flask import render_template
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


@app.route("/number/<int:n>", strict_slashes=False)
def number_route(n):
    """
    Function that displays 'n' as a number.
    """
    return "%i is a number" % n


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """
    Function that displays a HTML page only if n is an int.
    """
    return render_template('5-number.html', n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
