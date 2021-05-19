from flask import Flask
from flask_restful import Api
from items import Item, ItemList
from users import UserRegister
from flask_jwt import JWT
from sequrity import authenticate, identity


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'super-secret'
jwt = JWT(app, authenticate, identity)


api.add_resource(ItemList, "/items")
api.add_resource(Item, '/items/<string:name>')
api.add_resource(UserRegister, '/register')


if __name__ == "__main__":
    app.run(debug=True)
