from flask import Flask, jsonify, request
from flask_restful import Resource, Api

store = [
    {'name': "chair", 'price': 1500},
    {'name': "cupboard", 'price': 3000},
]

app = Flask(__name__)
api = Api(app)


class ItemList(Resource):
    def get(self):
        return jsonify(store)

    def post(self, data):
        pass


class Item(Resource):
    def get(self, name):
        asked_item = tuple(filter(lambda i: i['name'] == name, store))
        if len(asked_item) == 1:
            return asked_item[0]
        elif asked_item == ():
            return jsonify({'message': "Item wasn't found"})
        else:
            return jsonify({'message': "Database error"})
        # return jsonify({'type': str(type(asked_item)), 'value': str(asked_item)})

    def post(self, name):
        pass

    def delete(self, name):
        pass


api.add_resource(ItemList, "/items")
api.add_resource(Item, '/items/<string:name>')


if __name__ == "__main__":
    app.run(debug=True)
