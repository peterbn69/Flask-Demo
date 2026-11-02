import uuid

from flask_smorest import abort

def exists(old: dict, new: dict, *keys: str) -> None:
    for item in old.values():
        if all(item[key] == new[key] for key in keys):
            abort(400, message="Bad request. The element already exists.")

def respond(code: int, msg: str) -> None:
    abort(code, message = msg)

def get_or_404(collection: dict, record_id: str, label: str) -> dict:
    try:
        return collection[record_id]
    except KeyError:
        respond(404, f"{label} not found.")

def create(collection: dict, data: dict) -> dict:
    record_id = uuid.uuid4().hex
    record = {**data, "id": record_id}
    collection[record_id] = record
    return record

def delete_or_404(collection: dict, record_id: str, label: str) -> None:
    try:
        del collection[record_id]
        return {"message": f"{label} deleted."}
    except KeyError:
        respond(404, f"{label} not found.")
