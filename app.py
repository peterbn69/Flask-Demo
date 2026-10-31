from flask import Flask

from hello import hello_bp

app = Flask(__name__)
app.register_blueprint(hello_bp)