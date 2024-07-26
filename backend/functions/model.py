from pydantic import BaseModel
#from pathlib import Path

class Message(BaseModel):
    query: str
    chat_history_json_path: str

class DBModel(BaseModel):
    book_name: str
    text: str
    embeddings: list[float]