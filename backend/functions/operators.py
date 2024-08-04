from bson import ObjectId
from bcrypt import hashpw, gensalt, checkpw
from datetime import datetime, timedelta, timezone
import jwt
from jwt import PyJWTError

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from dbmodels import UserModel, UpdateUserModel
from dataset import collection_Users
from enviroment import JWT_SECRET_KEY, JWT_ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')

class CRUDOperator:

    async def read_all_users(self):
        tasks = []
        cursor = collection_Users.find({})
        async for document in cursor:
            tasks.append(UserModel(**document))
        return tasks

    async def read_one_user_by_id(self, id):
        task = await collection_Users.find_one({"_id": ObjectId(id)})
        return task

    async def read_one_user_by_name(self, username):
        task = await collection_Users.find_one({"username": username})
        return task

    async def read_one_user_by_email(self, email):
        task = await collection_Users.find_one({"email": email})
        return task

    async def create_user(self, task):
        task["password"] =  await JWTOperator().hash_password(task["password"])
        new_task = await collection_Users.insert_one(task)
        created_task = await collection_Users.find_one({"_id": new_task.inserted_id})
        return created_task

    async def update_user_by_id(self, id: str, data: UpdateUserModel):
        task = {k: v for k, v in data.model_dump().items() if v is not None}
        await collection_Users.update_one({"_id": ObjectId(id)}, {"$set": task})
        document = await collection_Users.find_one({"_id": ObjectId(id)})
        return document

    async def update_user_by_user(self, username: str, data: UpdateUserModel):
        task = {k: v for k, v in data.model_dump().items() if v is not None}
        await collection_Users.update_one({"username": username}, {"$set": task})
        document = await collection_Users.find_one({"username": username})
        return document

    async def update_user_chat(self, username: str, chat: dict[str, list[dict]]):
        await collection_Users.update_one({"username": username}, {"$set": {"chats": chat}})
        document = await collection_Users.find_one({"username": username})
        return document

class JWTOperator:
    def __init__(self):
        self.http_exception = HTTPException(401, "Could not validate credentials", headers=
                                {"WWW-Authenticate": "Bearer"})

    async def hash_password(self, password: str) -> str:
        hashed = hashpw(password.encode('utf-8'), gensalt())
        return hashed.decode('utf-8')

    async def verify_password(self, password: str, hashed_password: str) -> bool:
        return checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    async def authenticate_user(self, username: str, password: str) -> dict:
        user = await CRUDOperator().read_one_user_by_name(username)
        if not user:
            raise self.http_exception
        if not await self.verify_password(password, user["password"]):
            raise self.http_exception
        return user

    async def create_token(self, data: dict, time_expires: datetime | None = None) -> str:
        data_copy = data.copy()
        if time_expires is None:
            expires = datetime.now(timezone.utc) + timedelta(minutes=15)
        else:
            expires = datetime.now(timezone.utc) + time_expires
        data_copy.update({"exp": expires})
        token_jwt = jwt.encode(data_copy, key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return token_jwt
    
    async def create_user(self, username: str, password: str) -> dict:
        user = await CRUDOperator().create_user({"username": username, "password": password})
        return user
    
    async def validate_token(self, token: str = Depends(oauth2_scheme)) -> UserModel:
        try:
            payload = jwt.decode(token, key=JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            username = payload.get("sub")
            if username is None: 
                raise self.http_exception
        except PyJWTError:
            raise self.http_exception
        user = await CRUDOperator().read_one_user_by_name(username)
        if not user:
            raise self.http_exception
        return UserModel(**user)