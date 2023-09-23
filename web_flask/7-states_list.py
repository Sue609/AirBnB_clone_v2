#!/usr/bin/python3
"""
This module introduces a new function.
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def close_session(exception):
    """
    Function that closes the current SQLAlchemy session
    after each request.
    """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def fetch_data(storage):
    """
    Function that displays HTML page indise the bodt tag.
    """
    states = storage.all("State")
    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
