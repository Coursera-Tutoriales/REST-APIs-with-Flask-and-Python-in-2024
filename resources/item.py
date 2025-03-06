import os
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from utils.error_handler import get_error_message
from db import db
from models import ItemModel as ObjectModel
from models import StoreModel
from schemas import MessageSchema 
from schemas import ItemSchema as Schema
from schemas import ItemUpdateSchema as UpdateSchema


blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route("/item", methods=["GET", "POST"])
@blp.route("/item/<string:id>", methods=["GET", "PUT", "DELETE"])
class Item(MethodView):
    ########################## CREATE ##########################
    @blp.arguments(Schema)
    @blp.response(201, Schema)
    def post(self, data):
        store = StoreModel.query.get(data["store_id"])    
        if not store:
            abort(404, message=get_error_message("The specified store does not exist."))

        x = ObjectModel(**data)        
        try:        
            db.session.add(x)    
            db.session.commit()
            return x
        except IntegrityError as e:
            db.session.rollback()
            abort(400, message=get_error_message("An element with that name already exists.", e))
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=get_error_message("A database error occurred.", e))

    ######################### RETRIEVE #########################
    @blp.response(200, Schema(many=True))
    def get(self, id=None):
        if id:
            x = ObjectModel.query.get_or_404(id)
            return [x]
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            x = ObjectModel.query.order_by(ObjectModel.name).paginate(page=page, per_page=per_page)
            return x.items
        except SQLAlchemyError as e:
            abort(500, message=get_error_message("Error retrieving elements.", e))

    ######################### UPDATE BY ID #####################
    @blp.arguments(UpdateSchema)
    @blp.response(200, Schema)
    def put(self, data, id):
        x = ObjectModel.query.get_or_404(id, description="Element not found")
        if data:
            try:
                ObjectModel.query.filter_by(id=id).update(data)
                db.session.commit()
                db.session.refresh(x)

            except IntegrityError as e:
                db.session.rollback()
                abort(400, message=get_error_message("An Element with that name already exists.", e))
            except SQLAlchemyError as e:
                db.session.rollback()
                abort(500, message=get_error_message("An error occurred while updating the element.", e))

        return x

