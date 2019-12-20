import traceback
from datetime import datetime
from db import db
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from models.invoice import InvoiceModel
from schemas.invoice import InvoiceSchema

from libs.strings import gettext
from models.user import UserModel
from models.items import ItemsModel

invoice_schema = InvoiceSchema()
invoice_list_schema = InvoiceSchema(many=True)



class InvoiceRegister(Resource):
    @classmethod
    def post(cls):
        invoice_json = request.get_json()
        invoice = invoice_schema.load(invoice_json)



        if InvoiceModel.find_by_ref(invoice.ref_number):
            return {"message": gettext("invoice_ref_exists")}, 400

        try:
            now = datetime.now()
            invoice.create_at = now.strftime("%d/%m/%Y %H:%M:%S")
            invoice.created_by = 1

            invoice.save_to_db()
            return {"message": gettext("invoice_registered")}, 201
        except:
            traceback.print_exc()
            invoice.delete_from_db()
            return {"message": gettext("invoice_error_adding")}, 500


class Invoice(Resource):
    @classmethod
    def get(cls, id: int):
        invoice = InvoiceModel.find_by_id(id)

        if invoice:
            invoice.calc_sum()

        if invoice:
            return invoice_schema.dump(invoice), 200

        return {"message": gettext("invoice_not_found")}, 404

    @classmethod
    def post(cls, ref_number: int):
        if InvoiceModel.find_by_ref(ref_number):
            return {"message": gettext("invoice_ref_exists").format(ref_number)}, 400

        invoice_json = request.get_json()
        invoice_json["ref_number"] = ref_number

        invoice = invoice_schema.load(invoice_json)

        try:
            invoice.save_to_db()
        except:
            return {"message": gettext("invoice_error_inserting")}, 500

        return invoice_schema.dump(invoice), 201

    @classmethod
    def delete(cls, id: int):
        invoice = InvoiceModel.find_by_id(id)
        print(invoice)
        if invoice:
            invoice.delete_from_db()
            return {"message": gettext("invoice_deleted")}, 200

        return {"message": gettext("invoice_not_found")}, 404

    @classmethod
    def put(cls, ref_number: int):
        invoice_json = request.get_json()
        invoice = InvoiceModel.find_by_ref(ref_number)

        if invoice:
            invoice.client_id = invoice_json["client_id"]
        else:
            invoice_json["ref_number"] = ref_number
            invoice = invoice_schema.load(invoice_json)

        invoice.save_to_db()
        return invoice_schema.dump(invoice), 200


class InvoiceList(Resource):
    @classmethod
    def get(cls):
        return {"invoices": invoice_list_schema.dump(InvoiceModel.find_all())}, 200
