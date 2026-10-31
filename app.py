from flask import Flask, request

from greet import greet_bp
from store import store_bp

app = Flask(__name__)
app.register_blueprint(greet_bp)
app.register_blueprint(store_bp)