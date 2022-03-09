from flask import Flask
import torch

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"