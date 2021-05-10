from flask import Blueprint

from views import ManageSelfUser, ManageUsers, LogoutUser


users_blueprint = Blueprint("users", __name__, url_prefix="/users")


users_blueprint.add_url_rule(
    "/register", view_func=ManageUsers.as_view("register_user"), methods=["POST"]
)

users_blueprint.add_url_rule(
    "", view_func=ManageSelfUser.as_view("auth"), methods=["POST", "GET"]
)

users_blueprint.add_url_rule(
    "/logout", view_func=LogoutUser.as_view("logout"), methods=["PATCH"]
)

