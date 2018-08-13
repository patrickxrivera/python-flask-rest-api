from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        'name': 'Complete Life Optimization',
        'items': [
            {
                'name': 'Bulletproof Coffe',
                'price': 20.99
            }
        ]
    }
]

@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

def find_target_store(target_store_name):
    def find(store):
        return store['name'] == target_store_name
    return find

@app.route('/store/<string:name>')
def get_store(name):
    target_store = list(filter(find_target_store(name), stores))
    return jsonify({'store': target_store}) if target_store else jsonify({'message': 'No store found with that name.'})

@app.route('/stores')
def get_stores():
    return jsonify({'stores': stores})

@app.route('/store/<string:name>/item')
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            jsonify({'new_item': new_item})
    return jsonify({'message': 'store not found'})

@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if name == store['name']:
            return jsonify({'store': store['items']})
    return jsonify({ message: 'No store found with that name.' })

app.run(port=5000)
