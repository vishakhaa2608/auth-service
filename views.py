import json
import jwt
import traceback

from flask.views import MethodView
from flask import request, jsonify, make_response

from decorators import jwt_required, get_jwt_identity, create_access_token
from handlers import UserHandler


class ManageUsers(MethodView):
    def post(self):
        """Registers a user.

        Returns:
            Details of user and access token.
        """
        data = json.loads(request.get_data())
        user_handler = UserHandler()
        user_id, additional_id = user_handler.create_user(data)
        
        identity = {"id": user_id, "additionalId": additional_id}
        response = {
            "data": {
                "token": create_access_token(payload=identity, expires_delta=False),
                "user_id": user_id,
            }
        }

        return make_response(jsonify(response), 201)


class ManageSelfUser(MethodView):
    @jwt_required
    def get(self):
        """Fetch details of logged in user.

        Returns:
            A user object.
        """
        identity = get_jwt_identity()
        user_handler = UserHandler()
        user = user_handler.user_table.find_one({"id": identity["id"]}, {"_id": 0})
        print(user)
        if not user:
            response = {
                "error": "User not found or authentication token has expired. Try login again."
            }
            return make_response(jsonify(response), 404)
        return make_response(jsonify({"data": user}), 200)

    def post(self):
        """Logins a user.

        Returns:
           Returns auth token created.
        """
        data = json.loads(request.get_data())

        user = user = user_handler.user_table.find_one({"id": identity["id"]})
        if user:
            identity = identity = {
                "id": user["id"],
                "additionalId": user["additionalId"],
            }
            response = {
                "data": {
                    "token": create_access_token(
                        identity=identity, expires_delta=False
                    )
                }
            }
            return make_response(jsonify(response), 200)
        else:
            response = {"error": "User not found."}
            return make_response(jsonify(response), 404)

class LogoutUser(MethodView):
    @jwt_required
    def patch(self):
        """Logout user.
        """
        identity = get_jwt_identity()
        user_handler = UserHandler()
        user = user_handler.user_table.find_one({"id": identity["id"]})
        if not user:
            response = {"error": "User not found. Couldn't logout."}
            return make_response(jsonify(response), 404)

        jwt_token = request.environ.get("HTTP_AUTHORIZATION").split(" ")[-1]
        user_handler.blacklist_token({"id": identity["id"]}, jwt_token)
        response = {"message": "Logged out successfully."}
        return make_response(jsonify(response), 200)
