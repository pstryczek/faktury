# from flask import Flask, render_template, request,redirect
#
# app = Flask(__name__)
#
# email_addresses = []
# @app.route('/')
# def hello_world():
#     author="me"
#     name="you"
#     return render_template('index.html', author=author, name=name)
#
# @app.route('/signup', methods = ['POST'])
# def signup():
#     email = request.form['email']
#     email_addresses.append(email)
#     print(email_addresses)
#     return redirect('/')
#
# @app.route('/emails.html')
# def emails():
#     return render_template('emails.html', email_addresses=email_addresses)
#
# if __name__ == '__main__':
#     app.run()

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError

# from flask_uploads import configure_uploads, patch_request_class
from dotenv import load_dotenv

from db import db
from ma import ma
from blacklist import BLACKLIST
from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout
# from resources.items import Item, ItemList
# from resources.invoice import InvoiceList, Invoice, InvoiceRegister
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.addresses import Address, AddressList

app = Flask(__name__)
load_dotenv(".env", verbose=True)
app.config.from_object("default_config")  # load default configs from default_config.py
app.config.from_envvar(
    "APPLICATION_SETTINGS"
)  # override with config.py (APPLICATION_SETTINGS points to config.py)
# patch_request_class(app, 10 * 1024 * 1024)  # restrict max upload image size to 10MB
# configure_uploads(app, IMAGE_SET)
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


jwt = JWTManager(app)


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


# api.add_resource(Item, "/item/<string:name>")
# api.add_resource(ItemList, "/items")
#
# api.add_resource(InvoiceRegister, "/invoice/register")
# api.add_resource(Invoice, "/invoice/<int:ref_number>")
# api.add_resource(InvoiceList, "/invoices")

api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")

api.add_resource(Confirmation, "/user_confirm/<string:confirmation_id>")
api.add_resource(ConfirmationByUser, "/confirmation/user/<int:user_id>")

api.add_resource(Address, "/address/<string:address>")
api.add_resource(AddressList, "/addresses")


if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
