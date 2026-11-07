from flask_smorest import abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.extensions import db


def abort_with(code, message):
    abort(code, message=message)


def message_response(code, message):
    return {"message": message}, code


def commit_or_abort(error_message, conflict_message=None):
    try:
        db.session.commit()
    except SQLAlchemyError as exc:
        db.session.rollback()
        if conflict_message is not None and isinstance(exc, IntegrityError):
            abort_with(409, conflict_message)
        abort_with(500, error_message)
