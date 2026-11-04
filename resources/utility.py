from flask_smorest import abort

def respond(code: int, msg: str) -> None:
    abort(code, message = msg)

def message_response(code: int, msg: str) -> tuple[dict, int]:
    return {"message": msg}, code
