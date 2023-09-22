#!/usr/bin/python3
"""
This module introduces two functions.
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Script that displays "hello HBNB".
    """
    return "Hello HBNB"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Script that displays HBNB
    """
    return "HBNB"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=500)
