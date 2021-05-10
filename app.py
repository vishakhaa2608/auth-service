from flask import Flask, jsonify, make_response, request
# from flask_jwt_extended import JWTManager

from handlers import UserHandler
from config import JWT_SECRET_KEY, client

app = Flask(__name__)

from urls import users_blueprint

app.register_blueprint(users_blueprint)

app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
# app.config['JWT_BLACKLIST_ENABLED'] = True
# app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

# jwt = JWTManager(app)

# @jwt.unauthorized_loader
# def unauthorized_response(callback):
#     response = {"message": "Missing Authorization Header"}
#     return make_response(jsonify(response), 401)

# @jwt.token_in_blacklist_loader
# def check_token_in_blacklist(decrypted_token):
#     auth_token = request.environ.get("HTTP_AUTHORIZATION").split(" ")[-1]
#     user_handler = UserHandler()
#     identity = decrypted_token['identity']
#     user = user_handler.user_table.find_one({"id": identity["id"]})
#     blacklist = user.get("blacklistedTokens", [])
#     if auth_token in blacklist:
#         response = {"message": "The token provided has expired."}
#         return make_response(jsonify(response), 401)
