from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, fresh_jwt_required
from models.organization import OrganizationModel
from schemas.organization import OrganizationSchema
from libs.strings import gettext


organization_schema = OrganizationSchema()
organization_list_schema = OrganizationSchema(many=True)


class Organization(Resource):
    @classmethod
    def get(cls, name: str):
        organization = OrganizationModel.find_by_name(name)
        if organization:
            return organization_schema.dump(organization), 200

        return {"message": gettext("organization_not_found")}, 404

    @classmethod
    def post(cls, name: str):
        if OrganizationModel.find_by_name(name):
            return {"message": gettext("organization_name_exists").format(name)}, 400

        organization = OrganizationModel(name=name)
        try:
            organization.save_to_db()
        except:
            return {"message": gettext("organization_error_inserting")}, 500

        return organization_schema.dump(organization), 201


        # organization_json = request.get_json()
        # organization_json["name"] = name
        #
        # organization = organization_schema.load(organization_json)
        # try:
        #     organization.save_to_db()
        # except:
        #     return {"message": gettext("organization_error_inserting")}, 500
        #
        # return organization_schema.dump(organization), 201

    @classmethod
    @jwt_required
    def delete(cls, name: str):
        organization = OrganizationModel.find_by_name(name)
        if organization:
            organization.delete_from_db()
            return {"message": gettext("organization_deleted")}, 200

        return {"message": gettext("organization_not_found")}, 404

    # @classmethod
    # def put(cls, name: str):
    #     organization_json = request.get_json()
    #     organization = OrganizationModel.find_by_name(name)
    #
    #     if organization:
    #         organization.address = organization_json["address"]
    #     else:
    #         organization_json["name"] = name
    #         organization = organization_schema.load(organization_json)
    #
    #     organization.save_to_db()
    #
    #     return organization_schema.dump(organization), 200


class OrganizationList(Resource):
    @classmethod
    def get(cls):
        return {"organizations": organization_list_schema.dump(OrganizationModel.find_all())}, 200
