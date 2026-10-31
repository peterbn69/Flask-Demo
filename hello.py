from flask import Blueprint

hello_bp = Blueprint("hello", __name__)

@hello_bp.get("/hello")
def hello():
    return "Hello, World!"