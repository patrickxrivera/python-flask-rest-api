from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identify

app = Flask(__name__)
app.secret_key = 'patrick'
api = Api(app)
jwt = JWT(app, authenticate, identify)

items = []


def get_item_by(name):
    return next((i for i in items if i['name'] == name), None)


def create_item(name, data):
    return {'name': name, 'price': data['price']}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be blank!'
                        )

    @jwt_required()
    def get(self, name):
        item = get_item_by(name)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        item_exists = get_item_by(name)
        if item_exists:
            return {'error': 'Item with name {} already exists'.format(name)}, 400
        data = Item.parser.parse_args()
        item = create_item(name, data)
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = [item for item in items if item['name'] != name]
        return {'message': 'Item deleted.'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = get_item_by(name)
        if item:
            item.update(data)
        else:
            item = create_item(name, data)
            items.append(item)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
