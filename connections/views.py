from http import HTTPStatus

from flask import Blueprint, request
from marshmallow import ValidationError
from sqlalchemy.orm import joinedload
from webargs.flaskparser import use_args

from connections.models.connection import Connection, ConnectionType
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


@blueprint.route('/people/<person_id>/mutual_friends', methods=['GET'])
def get_friend(person_id):
    target_id = request.args.get('target_id')
    people_schema = PersonSchema(many=True)
    friend = Person.query.filter_by(
        id=target_id
    ).first_or_404()
    people = Person.query.options(
        joinedload('connections'),
    ).filter_by(
        id=person_id
    ).first_or_404().mutual_friends(friend)
    return people_schema.jsonify(people), HTTPStatus.OK


@blueprint.route('/connections', methods=['POST'])
@use_args(ConnectionSchema(), locations=('json',))
def create_connection(connection):
    try:
        connection.save()
    except ValidationError as err:
        return err.messages, HTTPStatus.BAD_REQUEST

    return ConnectionSchema().jsonify(connection), HTTPStatus.CREATED


@blueprint.route('/connections', methods=['GET'])
def get_connection():
    connection_schema = ConnectionSchema(many=True)
    connection = Connection.query.options(
        joinedload('from_person'),
        joinedload('to_person'),
    ).all()

    return connection_schema.jsonify(connection), HTTPStatus.OK


@blueprint.route('/connections/<connection_id>', methods=['PATCH'])
@use_args(ConnectionSchema(), locations=('json',))
def patch_connectionl(connection_type, connection_id):
    try:
        connection = Connection.query.filter_by(
            id=connection_id
        ).first_or_404()
        connection_schema = ConnectionSchema()
        new_velue = getattr(connection_type, 'connection_type', None)
        if new_velue and new_velue in ConnectionType:
            connection.update(connection_type=new_velue)
            connection.save()
    except ValidationError as err:
        return err.messages, HTTPStatus.BAD_REQUEST

    return connection_schema.jsonify(connection), HTTPStatus.OK
