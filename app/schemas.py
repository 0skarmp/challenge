from marshmallow import Schema, fields, validate

class ContactSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    lastname = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    address = fields.Str()
    reference_address = fields.Str()
    phone_number = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    