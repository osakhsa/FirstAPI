from flask import Flask
from flask_restful import Resource, Api, reqparse

store = [
    {'name': "chair", 'price': 1500},
    {'name': "cupboard", 'price': 3000},
]

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()


class ItemList(Resource):
    def get(self):
        return store

    def post(self, data):
        pass


class Item(Resource):
    def get(self, name):
        asked_item = tuple(filter(lambda i: i['name'] == name, store))
        if len(asked_item) == 1:
            return asked_item[0]
        elif asked_item == ():
            return {'message': "Item wasn't found"}, 405
        else:
            return {'message': "Database error"}, 500

    def post(self, name):
        asked_item = tuple(filter(lambda i: i['name'] == name, store))
        if asked_item == ():
            parser.add_argument('price')
            data = parser.parse_args()
            if not data['price']:
                return {'message': 'Price isn\'t given'}, 400
            new_item = {'name': name, 'price': data['price']}
            store.append(new_item)
            return new_item, 201
        else:
            return {'message': "Item already exists"}, 405

    def put(self, name):
        asked_item = tuple(filter(lambda i: i['name'] == name, store))
        parser.add_argument('price')
        data = parser.parse_args()
        if not data['price']:
            return {'message': 'Price isn\'t given'}, 400
        if asked_item == ():
            new_item = {'name': name, 'price': data['price']}
            store.append(new_item)
            return new_item, 201
        elif len(asked_item) > 1:
            return {'message': "Database error"}, 500
        else:
            price = data['price']
            asked_item[0]['price'] = price
            return asked_item[0], 201

    def delete(self, name):
        asked_item = tuple(filter(lambda i: i['name'] == name, store))
        if asked_item == ():
            return {'message': "Item wasn't found"}, 405
        elif len(asked_item) > 1:
            return {'message': "Database error"}, 500
        else:
            store.remove(asked_item[0])
            return {}, 204


api.add_resource(ItemList, "/items")
api.add_resource(Item, '/items/<string:name>')


if __name__ == "__main__":
    app.run(debug=True)
