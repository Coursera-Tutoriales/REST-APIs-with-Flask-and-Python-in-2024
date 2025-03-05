import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas.store import StoreSchema, StoreUpdateSchema

blp = Blueprint("Stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id], 200
        except KeyError:
            abort(404, message="Store not found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message":"store deleted"}
        except KeyError:
            abort(404, message="store not found")

    @blp.arguments(StoreUpdateSchema)
    def put(self, store_data, store_id):
        store_data = request.get_json()
        try:
            store = stores[store_id]
            store |= store_data
            return {"message":"store updated"}
        except KeyError:
            abort(404, message="store not found")

@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores":list(stores.values())}

    @blp.arguments(StoreSchema)
    def post(self, store_data):        
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message="Store already Exists")

        store_id = uuid.uuid4().hex
        store = {**store_data, "id":store_id}
        stores[store_id] = store
        return store, 201