from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from models.enums import State
from schemas.base import ComplaintBaseSchema


class ComplaintSchemaResponse(ComplaintBaseSchema):
    id = fields.Int(required=True)
    created_on = fields.DateTime(required=True)
    status = EnumField(State, by_value=True)
    photo_url = fields.URL(required=True)
    # complainer = fields.Nested()
