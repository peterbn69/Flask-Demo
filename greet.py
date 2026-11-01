from flask import Blueprint

greet_bp = Blueprint("greet", __name__)

@greet_bp.get("/hello")
def hello():
    return "Hello. Welcome to my first Python Flask project."

@greet_bp.get("/goodbye")
def goodbye():
    return "Goodbye. I hope you enjoy my Python Flask project."