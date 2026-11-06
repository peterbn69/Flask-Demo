from typing import NoReturn

from flask_smorest import abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db


def abort_with(code: int, message: str) -> NoReturn:
    abort(code, message=message)


def message_response(code: int, message: str) -> tuple[dict[str, str], int]:
    return {"message": message}, code


def commit_or_abort(error_message: str, conflict_message: str | None = None) -> None:
    try:
        db.session.commit()
    except SQLAlchemyError as exc:
        db.session.rollback()
        if conflict_message is not None and isinstance(exc, IntegrityError):
            abort_with(409, conflict_message)
        abort_with(500, error_message)
