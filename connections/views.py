from http import HTTPStatus

from flask import Blueprint
from marshmallow import ValidationError
from webargs.flaskparser import use_args

from connections.models.person import Person
from connections.schemas import ConnectionSchema, PersonSchema

blueprint = Blueprint('connections', __name__)


@blueprint.route('/people', methods=['GET'])
def get_people():
    people_schema = PersonSchema(many=True)
    people = Person.query.all()
    return people_schema.jsonify(people), HTTPStatus.OK


@blueprint.route('/people', methods=['POST'])
@use_args(PersonSchema(), locations=('json',))
def create_person(person):
    try:
        person.save()
    except ValidationError as err:
        return err.messages, HTTPStatus.BAD_REQUEST

    return PersonSchema().jsonify(person), HTTPStatus.CREATED


@blueprint.route('/connections', methods=['POST'])
@use_args(ConnectionSchema(), locations=('json',))
def create_connection(connection):
    try:
        connection.save()
    except ValidationError as err:
        return err.messages, HTTPStatus.BAD_REQUEST

    return ConnectionSchema().jsonify(connection), HTTPStatus.CREATED
