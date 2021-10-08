from http import HTTPStatus

from tests.factories import ConnectionFactory

EXPECTED_FIELDS = [
    'id',
    'connection_type',
    'from_person_id',
    'to_person_id',
    'from_person',
    'to_person',
]


def test_can_get_connection(db, testapp):
    ConnectionFactory.create_batch(10)
    db.session.commit()

    res = testapp.get('/connections')

    assert res.status_code == HTTPStatus.OK

    assert len(res.json) == 10
    for connection in res.json:
        for field in EXPECTED_FIELDS:
            assert field in connection
