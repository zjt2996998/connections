from http import HTTPStatus

from tests.factories import ConnectionFactory

from connections.models.connection import Connection

EXPECTED_FIELDS = [
    'id',
    'connection_type',
    'from_person_id',
    'to_person_id',
    'from_person',
    'to_person',
]


def test_can_update_connection(db, testapp):
    conn = ConnectionFactory.create_batch(1)
    db.session.commit()
    payload = {
        'connection_type': 'coworker',
    }
    res = testapp.patch('/connections/{id}'.format(id=conn[0].id), json=payload)

    assert res.status_code == HTTPStatus.OK

    connection = Connection.query.get(res.json['id'])
    assert connection is not None
    assert connection.connection_type.value == 'coworker'
