from marshmallow import fields

from schemas.base import ComplaintBaseSchema


class ComplaintSchemaRequest(ComplaintBaseSchema):
    photo = fields.String(required=True)
    photo_extension = fields.String(required=True)

