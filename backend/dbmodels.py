from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class Message(BaseModel):
    query: str
    chat_history: list[dict]

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, f):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return str(v)

class RAGModel(BaseModel):
    book_name: str
    text: str
    embeddings: list[float]

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    username: Optional[str] = Field(default=None)
    email: str
    password: str
    chats: dict[str, list[dict]]

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserCreateModel(BaseModel):
    username: Optional[str]
    email: str
    password: str
    chats: dict[str, list[dict]]

class UpdateUserModel(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    chats: Optional[dict[str, list[dict]]]

    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {ObjectId: str}