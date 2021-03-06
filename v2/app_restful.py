from flask import Flask
from flask_restful import Resource, Api, reqparse

store = [
    {'name': "chair", 'price': 1500},
    {'name': "cupboard", 'price': 3000},
]

app = Flask(__name__)
api = Api(app)


class ItemList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('items_to_add', type=dict, action="append")

    def get(self):
        return store

    def post(self):
        ready = []
        data = self.parser.parse_args()
        items_to_add = data['items_to_add']
        for i in items_to_add:
            item = dict(i)
            if 'name' in item and 'price' in item:
                    asked_item = tuple(filter(lambda i: i['name'] == item['name'], store))
                    if asked_item == ():
                        ready.append(i)
                    elif len(asked_item) != 1:
                        return {'message': "Database error"}, 500
        if ready == items_to_add:
            store.extend(ready)
            return store, 201
        elif not ready:
            return {'message': "All elements are given in incorrect form or exist in the store"}, 400
        else:
            store.extend(ready)
            return {'message': "Some elements are given in incorrect form or exist in the store",
                    'store': store}, 201


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', required=True)

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
            data = self.parser.parse_args()
            new_item = {'name': name, 'price': data['price']}
            store.append(new_item)
            return new_item, 201
        else:
            return {'message': "Item already exists"}, 405

    def put(self, name):
        asked_item = tuple(filter(lambda i: i['name'] == name, store))
        data = self.parser.parse_args()
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
