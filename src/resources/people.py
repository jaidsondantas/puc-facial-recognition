from flask_restful import Resource, reqparse
from bd import cursor, db


class People(Resource):
    attributes = reqparse.RequestParser()
    attributes.add_argument('name')

    def get(self):
        query = "SELECT * FROM people"
        cursor.execute(query)
        people = cursor.fetchall()

        return people

    def post(self):
        body = People.attributes.parse_args()
        query = "INSERT INTO people (name) VALUES (%s)"
        tuple = (body['name'])

        cursor.execute(query, tuple)
        db.commit()

        querySelect = "SELECT * from people where id = LAST_INSERT_ID()"
        cursor.execute(querySelect)

        return cursor.fetchone()
