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


api.add_resource(ItemList, "/items")


if __name__ == "__main__":
    app.run(debug=True)
