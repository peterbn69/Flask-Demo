from marshmallow import validate

NAME_MAX_LENGTH = 80
name_length = validate.Length(min=1, max=NAME_MAX_LENGTH)

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 128
password_length = validate.Length(min=PASSWORD_MIN_LENGTH, max=PASSWORD_MAX_LENGTH)
