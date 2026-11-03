from flask_smorest import abort

def respond(code: int, msg: str) -> None:
    abort(code, message = msg)
