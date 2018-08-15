from flask_restful import Resource, reqparse
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        return store.json() if store else {'message': 'Store not found'}, 404

    def post(self, name):
        existing_store = StoreModel.find_by_name(name)

        if existing_store:
            return {'message': 'Store named {} already exists'.format(name)}, 400

        new_store = StoreModel(name)

        try:
            new_store.save_to_db()
        except:
            return {'message': 'Error occured saving store to database.'}, 500

        return new_store.json(), 201

    def delete(self, name):
        existing_store = StoreModel.find_by_name(name)

        if not existing_store:
            return {'message': 'No store named {} exists'.format(name)}, 400

        try:
            existing_store.delete_from_db()
        except:
            return {'message': 'Error deleting store from database'}, 500

        return {'message': 'Store deleted.'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
