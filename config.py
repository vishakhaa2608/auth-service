import os
import pymongo

from dotenv import load_dotenv

load_dotenv(".env")

JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']

client = pymongo.MongoClient(
    "mongodb+srv://{user}:{password}@{cluster}/{db}?retryWrites=true&w=majority".format(
        user=os.environ.get("MONGO_USER"),
        password=os.environ.get("MONGO_PASSWORD"),
        cluster=os.environ.get("CLUSTER_URL"),
        db=os.environ.get("DB_NAME"),
    )
)
client = pymongo.MongoClient("0.0.0.0", 27017)
db = client[os.environ.get("DB_NAME")]

