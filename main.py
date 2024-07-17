import pymongo
import dotenv
import os

config = dotenv.dotenv_values(".env")

MONGO_CONNECTION = os.getenv(config["MONGO_CONNECTION"])
client = pymongo.MongoClient(MONGO_CONNECTION)




