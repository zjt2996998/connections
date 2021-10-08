from http import HTTPStatus

from tests.factories import ConnectionFactory, PersonFactory

EXPECTED_FIELDS = [
    'id',
    'first_name',
    'last_name',
    'email',
]


def test_can_get_people(db, testapp):
    PersonFactory.create_batch(10)
    db.session.commit()

    res = testapp.get('/people')

    assert res.status_code == HTTPStatus.OK

    assert len(res.json) == 10
    for person in res.json:
        for field in EXPECTED_FIELDS:
            assert field in person


def test_can_get_mutual_friends(db, testapp):
    instance = PersonFactory()
    target = PersonFactory()

    # some decoy connections (not mutual)
    ConnectionFactory.create_batch(5, to_person=instance)
    ConnectionFactory.create_batch(5, to_person=target)

    mutual_friends = PersonFactory.create_batch(3)
    for f in mutual_friends:
        ConnectionFactory(from_person=instance, to_person=f, connection_type='friend')
        ConnectionFactory(from_person=target, to_person=f, connection_type='friend')

    # mutual connections, but not friends
    decoy = PersonFactory()
    ConnectionFactory(from_person=instance, to_person=decoy, connection_type='coworker')
    ConnectionFactory(from_person=target, to_person=decoy, connection_type='coworker')

    db.session.commit()
    res = testapp.get('/people/{person_id}/mutual_friends?target_id={target_id}'.format(
        person_id=instance.id,
        target_id=target.id,
    ))
    assert len(res.json) == len(mutual_friends)
    assert res.status_code == HTTPStatus.OK
    expected_mutual_friend_ids = [f.id for f in mutual_friends]
    actual_mutual_friend_ids = [p['id'] for p in res.json]
    assert actual_mutual_friend_ids == expected_mutual_friend_ids
