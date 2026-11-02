from flask import Flask, request

from resources.store import store_bp
from resources.item import item_bp

app = Flask(__name__)
app.register_blueprint(store_bp)
app.register_blueprint(item_bp)
