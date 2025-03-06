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
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    @blp.response(200, MessageSchema)
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id, description="Store not found")

        try:
            db.session.delete(store)
            db.session.flush()   # ⚠️ Detecta errores de integridad antes de commit()
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            abort(400, message=get_error_message("Cannot delete the store because it has related records.", e))
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=get_error_message("An error occurred while deleting the store.", e))

        return {"message": "Store deleted successfully"}

    @blp.arguments(StoreUpdateSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        store = StoreModel.query.get_or_404(store_id, description="Store not found")
        if store_data:  # Solo actualiza si hay datos
            try:
# ✅ Más eficiente: ejecuta una única consulta UPDATE, ideal para múltiples registros.  
# ⚠️ No actualiza en memoria (se usa db.session.refresh(store)), puede omitir validaciones y afectar relaciones.  

                StoreModel.query.filter_by(id=store_id).update(store_data)
                db.session.commit()
                db.session.refresh(store)

# ✅ Ejecuta validaciones, mantiene relaciones y actualiza en memoria sin refresh().  
# ⚠️ Menos eficiente con muchos campos (genera múltiples consultas UPDATE).  

                #for key, value in store_data.items():
                #    setattr(store, key, value)
                #db.session.commit()

            except IntegrityError as e:
                db.session.rollback()
                abort(400, message=get_error_message("A store with that name already exists.", e))
            except SQLAlchemyError as e:
                db.session.rollback()
                abort(500, message=get_error_message("An error occurred while updating the store.", e))

        return store

@blp.route("/store")
class StoreList(MethodView):

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        try:
            return StoreModel.query.order_by(StoreModel.name).all()  # Ordenar por nombre
        except SQLAlchemyError as e:
            abort(500, message=get_error_message("Error retrieving stores.", e))

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
        