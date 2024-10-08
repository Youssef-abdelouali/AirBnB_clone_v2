#!/usr/bin/python3
"""
This module contains a simple Flask application that listens on 0.0.0.0:5000
and displays "Hello HBNB!" when accessing the root URL.
"""

from flask import Flask

app = Flask(__name__)

@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Display a simple message 'Hello HBNB!'"""
    return "Hello HBNB!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
