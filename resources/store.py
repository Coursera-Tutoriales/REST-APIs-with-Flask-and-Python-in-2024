import os
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from utils.error_handler import get_error_message
from db import db
from models import StoreModel
from schemas import MessageSchema, StoreSchema, StoreUpdateSchema

blp = Blueprint("Stores", __name__, description="Operations on stores")

@blp.route("/store", methods=["GET", "POST"])
@blp.route("/store/<string:store_id>", methods=["GET", "PUT", "DELETE"])
class Store(MethodView):
    ########################## CREATE ##########################
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):        
        store = StoreModel(**store_data)        
        try:        
            db.session.add(store)    
            db.session.commit()
            return store
        except IntegrityError as e:
            db.session.rollback()
            abort(400, message=get_error_message("A store with that name already exists.", e))
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=get_error_message("A database error occurred.", e))

    ######################### RETRIEVE #########################
    @blp.response(200, StoreSchema(many=True))
    def get(self, store_id=None):
        if store_id:
            store = StoreModel.query.get_or_404(store_id)
            return [store]
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            stores = StoreModel.query.order_by(StoreModel.name).paginate(page=page, per_page=per_page)
            return stores.items
        except SQLAlchemyError as e:
            abort(500, message=get_error_message("Error retrieving stores.", e))

    ######################### UPDATE BY ID #####################
    @blp.arguments(StoreUpdateSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        store = StoreModel.query.get_or_404(store_id, description="Store not found")
        if store_data:
            try:
                StoreModel.query.filter_by(id=store_id).update(store_data)
                db.session.commit()
                db.session.refresh(store)

            except IntegrityError as e:
                db.session.rollback()
                abort(400, message=get_error_message("A store with that name already exists.", e))
            except SQLAlchemyError as e:
                db.session.rollback()
                abort(500, message=get_error_message("An error occurred while updating the store.", e))

        return store
    ######################### DELETE BY ID #####################
    @blp.response(200, MessageSchema)
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id, description="Store not found")
        try:
            db.session.delete(store)
            db.session.flush()
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            abort(400, message=get_error_message("Cannot delete the store because it has related records.", e))
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=get_error_message("An error occurred while deleting the store.", e))

        return {"message": "Store deleted successfully"}

   