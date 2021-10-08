from datetime import date

from marshmallow import fields, validates_schema, ValidationError
from marshmallow_enum import EnumField

from connections.extensions import ma
from connections.models.connection import Connection, ConnectionType
from connections.models.person import Person


TODAY = date.today()


class BaseModelSchema(ma.ModelSchema):

    def __init__(self, strict=True, **kwargs):
        super().__init__(strict=strict, **kwargs)


class PersonSchema(BaseModelSchema):

    id = fields.Integer()
    first_name = fields.Str(
        required=True,
        error_messages={'required': 'missing first name'},
    )
    last_name = fields.Str()
    email = fields.Email(
        required=True,
        error_messages={'required': 'missing email'},
    )
    date_of_birth = fields.Date(
        validate=lambda x: x < TODAY,
        error_messages={'validator_failed': 'Cannot be in the future.'},
    )

    class Meta:
        model = Person


class ConnectionSchema(BaseModelSchema):
    from_person_id = fields.Integer()
    to_person_id = fields.Integer()
    connection_type = EnumField(ConnectionType)
    from_person = fields.Nested(
        PersonSchema,
        only=['id', 'first_name', 'last_name', 'email', 'date_of_birth'],
        dump_only=True,
    )
    to_person = fields.Nested(
        PersonSchema,
        only=['id', 'first_name', 'last_name', 'email', 'date_of_birth'],
        dump_only=True,
    )

    @validates_schema()
    def validate_object(self, data):
        if 'from_person_id' in data and 'to_person_id' in data:
            from_person = Person.query.get(data['from_person_id']).date_of_birth
            to_person = Person.query.get(data['to_person_id']).date_of_birth
            if from_person <= to_person:
                if data['connection_type'] is ConnectionType.son:
                    raise ValidationError('Invalid connection - son older than parent.')
                elif data['connection_type'] is ConnectionType.daughter:
                    raise ValidationError('Invalid connection - daughter older than parent.')
            if from_person >= to_person:
                if data['connection_type'] is ConnectionType.father:
                    raise ValidationError('Invalid connection - father younger than child.')
                elif data['connection_type'] is ConnectionType.mother:
                    raise ValidationError('Invalid connection - mother younger than child.')

    class Meta:
        model = Connection
