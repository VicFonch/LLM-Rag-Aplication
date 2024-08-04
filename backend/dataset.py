from motor.motor_asyncio import AsyncIOMotorClient
from enviroment import MONGO_URI, DB_NAME

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection_VectorCronology = db["VectorCronology"]
collection_Users = db["Users"]