from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db

hasher = PasswordHasher()


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


def hash_password(password):
    return hasher.hash(password)


def verify_password(password, stored_hash):
    try:
        return hasher.verify(stored_hash, password)
    except VerificationError:
        return False
