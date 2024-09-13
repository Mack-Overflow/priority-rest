from marshmallow import Schema, fields, validate, ValidationError

class CustomerSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))
    phone = fields.Str(required=True, validate=validate.Regexp(r'^\+?1?\d{9,15}$'))
    state = fields.Str(required=True, validate=validate.Length(min=2))

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=6))

user_schema = UserSchema()
users_schema = UserSchema(many=True)
