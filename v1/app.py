from flask import Flask, jsonify, request


app = Flask(__name__)


stores = [
    {
        'name': 'My Store',
        'items': [
            {
                'name': 'chair',
                'price': 1500
            }
        ]
    }
]


# POST /store -> name
@app.route('/store', methods=['POST'])
def create_store():
    data = request.get_json()
    try:
        name = data['name']
    except KeyError:
        return wfields_response
    store = {
        'name': name,
        'items': []
    }
    stores.append(store)
    return store


# GET /store/<name>
@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'store not found'})


# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})


# POST /store/<name>/item -> name, price
@app.route('/store/<string:store_name>/item', methods=["POST"])
def add_item(store_name):
    data = request.get_json()
    for store in stores:
        if store['name'] == store_name:
            try:
                name = data['name']
                price = data['price']
            except KeyError:
                return wfields_response
            store['items'].append({'name': name, 'price': price})
            return store
    return storenf_response


# GET /store/<name>/item
@app.route('/store/<string:name>/item')
def get_items(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store['items'])
    return jsonify(storenf_response)


if __name__ == '__main__':
    storenf_response = {'message': 'store is not found'}
    wfields_response = {'message': 'wrong field(s)'}
    app.run(debug=True)
