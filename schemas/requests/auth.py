from marshmallow import fields, Schema, validate

from schemas.base import AuthBase


class RegisterSchemaRequest(AuthBase):
    first_name = fields.Str(required=True, validate=validate.Length(min=2, max=20))
    last_name = fields.Str(required=True, validate=validate.Length(min=2, max=20))
    phone_number = fields.Str(required=True, validate=validate.Length(min=10, max=20))


class LoginSchemaRequest(AuthBase):
    # We are leaving this class empty, because it inherits the needed info (email and password)
    pass


