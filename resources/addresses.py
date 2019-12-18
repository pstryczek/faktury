from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, fresh_jwt_required
from models.addresses import AddressModel
from schemas.addresses import AddressSchema
from libs.strings import gettext


address_schema = AddressSchema()
address_list_schema = AddressSchema(many=True)


class Address(Resource):
    @classmethod
    def get(cls, address: str):
        addresses = AddressModel.find_by_name(address)
        if addresses:
            return address_schema.dump(addresses), 200

        return {"message": gettext("address_not_found")}, 404

    @classmethod
    def post(cls, address: str):
        if AddressModel.find_by_name(address):
            return {"message": gettext("address_name_exists").format(address)}, 400

        address_json = request.get_json()
        address_json["ci"] = address

        addresses = address_schema.load(address_json)

        try:
            addresses.save_to_db()
        except:
            return {"message": gettext("item_error_inserting")}, 500

        return address_schema.dump(addresses), 201

    @classmethod
    @jwt_required
    def delete(cls, address: str):
        addresses = AddressModel.find_by_name(address)
        if address:
            address.delete_from_db()
            return {"message": gettext("address_deleted")}, 200

        return {"message": gettext("address_not_found")}, 404

    @classmethod
    def put(cls, address: str):
        address_json = request.get_json()
        item = AddressModel.find_by_name(name)

        if address:
            address_json["address"] = address
            address = address_schema.load(address)

        address.save_to_db()

        return address_schema.dump(item), 200


class AddressList(Resource):
    @classmethod
    def get(cls):
        return {"Addresses": address_list_schema.dump(AddressModel.find_all())}, 200
