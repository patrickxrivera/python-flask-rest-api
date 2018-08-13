from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []


def get_item_by(name):
    return next(list(filter(lambda i: i['name'] == name, None)))


class Item(Resource):
    def get(self, name):
        item = get_item_by(name)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        data = request.get_json()
        item_exists = get_item_by(name)
        if item_exists:
            return {'error': 'Item with name {} already exists'.format(name)}, 400
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
