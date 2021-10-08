from connections.database import CreatedUpdatedMixin, CRUDMixin, db, Model
from connections.models.connection import ConnectionType


class Person(Model, CRUDMixin, CreatedUpdatedMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(145), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    connections = db.relationship('Connection', foreign_keys='Connection.from_person_id')

    def mutual_friends(self, person):
        mutual_friend = []
        for con in person.connections:
            if con.connection_type is ConnectionType.friend:
                mutual_friend.append(con.to_person)
        return mutual_friend
