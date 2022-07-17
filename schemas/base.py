from marshmallow import fields, validate, Schema


class AuthBase(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8, max=20))


class ComplaintBaseSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    amount = fields.Float(required=True)
    photo_url = fields.Str(required=True)
