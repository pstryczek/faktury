from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, fresh_jwt_required
from models.items import ItemsModel
from schemas.items import ItemsSchema
from libs.strings import gettext
import traceback

item_schema = ItemsSchema()
item_list_schema = ItemsSchema(many=True)

class ItemRegister(Resource):
    @classmethod
    def post(cls):
        item_json = request.get_json()
        item = item_schema.load(item_json)
        name = item.name
        if ItemsModel.find_by_name(name):
            return {"message": gettext("item_name_exists").format(name)}, 400

        try:
            item.save_to_db()
            return {"message": gettext("item_registered")}, 201
        except:
            traceback.print_exc()
            # item.delete_from_db()
            return {"message": gettext("item_error_adding")}, 500

class Item(Resource):
    @classmethod
    def get(cls, name: str):
        item = ItemsModel.find_by_name(name)
        if item:
            return item_schema.dump(item), 200

        return {"message": gettext("item_not_found")}, 404

    @classmethod
    def post(cls, name: str):
        if ItemsModel.find_by_name(name):
            return {"message": gettext("item_name_exists").format(name)}, 400

        item_json = request.get_json()
        item_json["name"] = name

        item = item_schema.load(item_json)

        try:
            item.save_to_db()
        except:
            return {"message": gettext("item_error_inserting")}, 500

        return item_schema.dump(item), 201

    @classmethod
    def delete(cls, name: str):
        item = ItemsModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": gettext("item_deleted")}, 200

        return {"message": gettext("item_not_found")}, 404

    @classmethod
    def put(cls, name: str):
        item_json = request.get_json()
        item = ItemsModel.find_by_name(name)

        if item:
            item.price = item_json["price"]
        else:
            item_json["name"] = name
            item = item_schema.load(item_json)

        item.save_to_db()

        return item_schema.dump(item), 200


class ItemList(Resource):
    @classmethod
    def get(cls):
        return {"items": item_list_schema.dump(ItemsModel.find_all())}, 200
