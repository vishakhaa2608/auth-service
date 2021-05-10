from time import time
from uuid import uuid4

from config import db


class UserHandler:
    def __init__(self):
        self.db = db
        self.user_table = self.db["Users"]

    def create_user(self, data):
        user_id = str(uuid4())
        additional_id = str(uuid4())
        data["additionalId"] = additional_id

        time_now = int(time() * 1000)

        self.user_table.insert(
            {
                "id": user_id,
                "additionalId": data["additionalId"],
                "displayName": data["displayName"],
                "email": data.get("email", ""),
                "provider": data["provider"],
                "photoURL": data.get("photoURL", ""),
                "createdAt": time_now,
            }
        )

        return user_id, additional_id

    def get_user(self, key, projection=None):

        if "id" in key:
            response = self.user_table.find({"id": key["id"]})

        elif "additionalId" in key:
            query = {"additionalId": key["additionalId"]}
            response = self.user_table.find(query)

        else:
            response = ({"message": "Query on id or additionalId."}, 400)
            log_custom_errors(response[0])
            return response

        return ({"data": response}, 200)


    def blacklist_token(self, identity, jwt_token):
        self.user_table.update_one(
            {"id": identity["id"]},
            {"$push": {"blacklistedTokens": jwt_token}}
        )