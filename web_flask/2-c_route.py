#!/usr/bin/python3
from flask import Flask
 
app = Flask(__name__)
 
@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Script that displays hello HBNB
    """
    return "Hello HBNB"
 
@app.route('/hbnb', strict_slashes=False)
def hbhn():
    """
    Script that displays hbnb
    """
    return "hbnb"

@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """
    Function that replaces underscore with spaces in the text.
    """
    text = text.replace("_", " ")
    return f"C {text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)