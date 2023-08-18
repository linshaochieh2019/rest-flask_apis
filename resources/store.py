import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
#from db import stores
from db import db
from models import StoreModel, TagModel
from schema import StoreSchema, TagSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route('/store')
class StoreList(MethodView):

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema) 
    @blp.response(200, StoreSchema)   
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message = "The store name is taken."
            )
        except SQLAlchemyError:
            abort(
                500,
                message = "An error occurred when inserting the data."
            )
        return store, 201

@blp.route('/store/<int:store_id>')
class Store(MethodView):

    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "The store is deleted."}
    

