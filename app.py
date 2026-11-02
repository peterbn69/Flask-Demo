from flask import Flask, request

from resources.store import bp as store_bp
from resources.item import bp as item_bp

app = Flask(__name__)

app.register_blueprint(store_bp)
app.register_blueprint(item_bp)
