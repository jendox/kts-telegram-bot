from marshmallow import Schema, post_dump, post_load


class BaseSchema(Schema):
    @post_load
    def make_object(self, data, **kwargs):
        if hasattr(self.Meta, "model"):
            return self.Meta.model(**data)
        return data

    @post_dump
    def remove_none(self, data, **kwargs) -> dict:
        return {k: v for k, v in data.items() if v is not None}
