from marshmallow import EXCLUDE, fields

from shared.client.schemes.base import BaseSchema
from shared.client.types import User

__all__ = ("UserSchema",)


class UserSchema(BaseSchema):
    class Meta:
        model = User
        unknown = EXCLUDE

    id = fields.Int(required=True)
    is_bot = fields.Bool(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(allow_none=True)
    username = fields.Str(allow_none=True)
