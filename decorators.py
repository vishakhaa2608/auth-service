import jwt

from flask import request, jsonify, make_response

from config import JWT_SECRET_KEY
from handlers import UserHandler


def create_access_token(payload, expires_delta):
    auth_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
    return auth_token


def get_jwt_identity():
    auth_token = request.environ.get("HTTP_AUTHORIZATION").split(" ")[-1]
    payload = jwt.decode(auth_token, JWT_SECRET_KEY, algorithms="HS256")
    return payload


def jwt_required(func):
    def inner(*args, **kwargs):
        identity = get_jwt_identity()
        user_handler = UserHandler()
        user = user_handler.user_table.find_one({"id": identity["id"]}, {"_id": 0})
        if not user:
            response = {
                "error": "Authentication token incorrect. Try logging in again."
            }
            return make_response(jsonify(response), 403)
        return func(*args, **kwargs)

    return inner
