from flask_restful import Resource, reqparse
import sqlite3
from flask_jwt import jwt_required


class ItemList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('items_to_add', type=dict, action="append")

    @staticmethod
    @jwt_required()
    def get():
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute('SELECT name, price FROM items')
        rows = cur.fetchall()
        con.close()
        all_items = []
        for row in rows:
            all_items.append({'name': row[0], 'price': row[1]})
        return all_items

    @jwt_required()
    def post(self):
        ready = []
        data = self.parser.parse_args()
        items_to_add = data['items_to_add']
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        for i in items_to_add:
            item = dict(i)
            if 'name' in item and 'price' in item:
                cur.execute(f'SELECT name, price FROM items WHERE name = "{item["name"]}"')
                asked_item = cur.fetchall()
                if not asked_item:
                    ready.append(item)
                elif len(asked_item) != 1:
                    return {'message': "Database error"}, 500
        if ready == items_to_add:
            for i in ready:
                cur.execute(f'INSERT INTO items (name, price) VALUES ("{i["name"]}", {i["price"]})')
            con.commit()
            con.close()
            content = self.get()
            return content, 201
        elif not ready:
            con.commit()
            con.close()
            return {'message': "All elements are given in incorrect form or exist in the store"}, 400
        else:
            for i in ready:
                cur.execute(f'INSERT INTO items (name, price) VALUES ("{i["name"]}", {i["price"]})')
            con.commit()
            con.close()
            content = self.get()
            return {'message': "Some elements are given in incorrect form or exist in the store",
                    'store': content}, 201


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', required=True)

    @staticmethod
    @jwt_required()
    def get(name):
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute(f'SELECT name, price FROM items WHERE name = "{name}"')
        asked_item = cur.fetchall()
        con.close()
        if len(asked_item) == 1:
            return {'name': asked_item[0][0], 'price': asked_item[0][1]}
        elif not asked_item:
            return {'message': "Item wasn't found"}, 405
        else:
            return {'message': "Database error"}, 500

    @jwt_required()
    def post(self, name):
        data = self.parser.parse_args()
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        try:
            cur.execute(f'INSERT INTO items (name, price) VALUES  ("{name}", {data["price"]})')
        except sqlite3.IntegrityError:
            con.close()
            return {'message': "Item already exists"}, 405
        con.commit()
        con.close()
        new_item = {'name': name, 'price': data['price']}
        return new_item, 201

    @jwt_required()
    def put(self, name):
        data = self.parser.parse_args()
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        try:
            cur.execute(f'INSERT INTO items (name, price) VALUES  ("{name}", {data["price"]})')
        except sqlite3.IntegrityError:
            cur.execute(f'UPDATE items SET price = {data["price"]} WHERE name = "{name}"')
            con.commit()
            con.close()
            return {'message': "Item updated successfully", 'item': {'name': name, 'price': data['price']}}, 201
        else:
            con.commit()
            con.close()
            return {'message': "Item added successfully", 'item': {'name': name, 'price': data['price']}}, 201

    @staticmethod
    @jwt_required()
    def delete(name):
        con = sqlite3.connect('data.db')
        cur = con.cursor()
        cur.execute(f'SELECT * FROM items WHERE name="{name}"')
        asked_item = cur.fetchall()
        if not asked_item:
            return {'message': "Item wasn't found"}, 405
        elif len(asked_item) > 1:
            return {'message': "Database error"}, 405
        cur.execute(f'DELETE FROM items WHERE name="{name}"')
        con.commit()
        con.close()
        return {}, 204
