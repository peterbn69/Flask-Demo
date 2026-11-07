from argon2 import PasswordHasher
from argon2.exceptions import VerificationError

hasher = PasswordHasher()


def hash_password(password):
    return hasher.hash(password)


def verify_password(password, stored_hash):
    try:
        return hasher.verify(stored_hash, password)
    except VerificationError:
        return False
