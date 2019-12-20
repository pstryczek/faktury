import traceback
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, fresh_jwt_required
from models.addresses import AddressModel
from schemas.addresses import AddressSchema
from libs.strings import gettext


address_schema = AddressSchema()
address_list_schema = AddressSchema(many=True)

class AddressRegister(Resource):
    @classmethod
    def post(cls):
        address_json = request.get_json()
        address = address_schema.load(address_json)

        if AddressModel.find_by_name(address.address):
            return {"message": gettext("address_exists").format(address.address)}, 400

        try:
            address.save_to_db()

            return {"message": gettext("address_registered")}, 201

        except:
            traceback.print_exc()
            address.delete_from_db()
            return {"message": gettext("address_error_creating")}, 500



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
            return {"message": gettext("address_exists").format(address)}, 400

        addresses = AddressModel(address=address)
        try:
            addresses.save_to_db()
        except:
            return {"message": gettext("address_error_inserting")}, 500

        return address_schema.dump(addresses), 201



        # if AddressModel.find_by_name(address):
        #     return {"message": gettext("address_name_exists").format(address)}, 400
        #
        # address_json = request.get_json()
        # address_json["address"] = address
        #
        # addresses = address_schema.load(address_json)
        #
        # try:
        #     addresses.save_to_db()
        # except:
        #     return {"message": gettext("address_error_inserting")}, 500
        #
        # return address_schema.dump(addresses), 201

    @classmethod
    def delete(cls, address: str):
        address = AddressModel.find_by_id(address)
        if not address:
            return {"message": gettext("address_not_found")}, 404

        address.delete_from_db()
        return {"message": gettext("address_deleted")}, 200

    @classmethod
    def put(cls, address: str):
        if AddressModel.find_by_name(address):
            return {"message": gettext("address_exists").format(address)}, 400

        addresses = AddressModel(address=address)
        try:
            addresses.save_to_db()
        except:
            return {"message": gettext("address_error_inserting")}, 500

        return address_schema.dump(addresses), 201




class AddressList(Resource):
    @classmethod
    def get(cls):
        return {"Addresses": address_list_schema.dump(AddressModel.find_all())}, 200
