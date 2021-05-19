from flask_restful import Resource, reqparse
import sqlite3


class User(object):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password


    @staticmethod
    def find_by_username(username):
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute(f'SELECT * FROM users WHERE username = "{username}"')
        asked_user = cur.fetchone()
        con.close()
        if asked_user:
            return User(*asked_user)

    @staticmethod
    def find_by_id(user_id):
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute(f'SELECT * FROM users WHERE id = "{user_id}"')
        asked_user = cur.fetchone()
        con.close()
        if asked_user:
            return User(*asked_user)


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True)
    parser.add_argument('password', required=True)

    def post(self):
        data = self.parser.parse_args()
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        try:
            cur.execute(f'INSERT INTO users (username, password) VALUES  ("{data["username"]}", "{data["password"]}")')
        except sqlite3.IntegrityError:
            con.close()
            return {'message': "User with this username already exists"}, 405
        con.commit()
        con.close()
        new_user = {'username': data["username"], 'password': data["password"]}
        return new_user, 201
