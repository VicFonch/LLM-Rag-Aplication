import os
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv

from dbmodels import UserModel, UpdateUserModel

load_dotenv("../.env")
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = "Users"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

async def read_all_users():
    tasks = []
    cursor = collection.find({})
    async for document in cursor:
        tasks.append(UserModel(**document))
    return tasks

async def read_one_user_by_id(id):
    task = await collection.find_one({"_id": ObjectId(id)})
    return task

async def read_one_user_by_name(username):
    task = await collection.find_one({"username": username})
    return task

async def read_one_user_by_email(email):
    task = await collection.find_one({"email": email})
    return task

async def create_user(task):
    new_task = await collection.insert_one(task)
    created_task = await collection.find_one({"_id": new_task.inserted_id})
    return created_task

async def update_user_by_id(id: str, data: UpdateUserModel):
    task = {k: v for k, v in data.model_dump().items() if v is not None}
    await collection.update_one({"_id": ObjectId(id)}, {"$set": task})
    document = await collection.find_one({"_id": ObjectId(id)})
    return document

async def update_user_by_user(username: str, data: UpdateUserModel):
    task = {k: v for k, v in data.model_dump().items() if v is not None}
    await collection.update_one({"username": username}, {"$set": task})
    document = await collection.find_one({"username": username})
    return document

async def update_user_chat(username: str, chat: dict[str, list[dict]]):
    await collection.update_one({"username": username}, {"$set": {"chats": chat}})
    document = await collection.find_one({"username": username})
    return document



