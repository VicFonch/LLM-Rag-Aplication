from dotenv import load_dotenv
import os, json
from motor.motor_asyncio import AsyncIOMotorClient
from typing import AsyncIterable
import asyncio

#from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models.ollama import ChatOllama
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain_core.messages.base import BaseMessage

#from functions.model import DBModel

load_dotenv("../.env")
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
ATLAS_VECTOR_SEARCH_INDEX_NAME = os.getenv("ATLAS_VECTOR_SEARCH_INDEX_NAME")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

async def perform_similarity_search(query: str, top_k: int=100) -> list[str]:
    try:
        if not all([MONGO_URI, DB_NAME, COLLECTION_NAME, ATLAS_VECTOR_SEARCH_INDEX_NAME, LLM_MODEL_NAME]):
            raise ValueError("Set the environment variables MONGO_URI, DB_NAME, COLLECTION_NAME, ATLAS_VECTOR_SEARCH_INDEX_NAME, and MODEL_NAME")
        
        embedding_model = OllamaEmbeddings(model=LLM_MODEL_NAME)
        pipeline = [
            {
                "$vectorSearch": {
                    "index": ATLAS_VECTOR_SEARCH_INDEX_NAME,
                    "path": "embeddings",
                    "queryVector": embedding_model.embed_query(query),
                    "numCandidates": 100,
                    "limit": top_k
                }
            }
        ]

        async with collection.aggregate(pipeline) as cursor:
            results = []
            async for doc in cursor:
                results.append(doc["text"])

        return results

    except Exception as e:
        print(f"Error during similarity search: {e}")
        return None

def get_message_history(chat_history_json_path: str) -> list[str]:
    try:
        with open(chat_history_json_path, 'r') as chat_history_file:
            data = json.load(chat_history_file)
            if len(data) > 5:
                chat_history = [chat for chat in data]
            else:
                chat_history = data[-5:]
        return chat_history
    except Exception as e:
        print(f"Error during loading chat histoy json: {e}")
        return None

async def prompt_engine(query: str, chat_history_json_path: str) -> list[BaseMessage]:

    chat_history = get_message_history(chat_history_json_path)
    
    messages = []

    context = """
        You are an asistent of a second world war general, 
        you are in a bunker and the general is asking you questions about the war.
        If you don't know the answer, say you don't know.
        Use three sentence maximum and keep the answer concise. 

        If is necessary, you can use the next information, but don't say that you are using it:
    """
    
    similar_search = await perform_similarity_search(query)
    context += "\n".join(similar_search)

    messages.append(SystemMessage(content=context))

    for entry in chat_history:
        if entry["role"] == "human":
            messages.append(HumanMessage(content=entry["content"]))
        elif entry["role"] == "ai":
            messages.append(AIMessage(content=entry["content"]))
        # elif entry["role"] == "system":
        #     messages.append(SystemMessage(content=entry["content"]))

        # Añadir la nueva consulta al historial
        messages.append(HumanMessage(content=query)) 

    return messages

async def streaming_response(query: str, chat_history_json_path: str) -> AsyncIterable[str]:

    messages = await prompt_engine(query, chat_history_json_path)

    # Invocar el modelo de chat con el historial completo
    callback = AsyncIteratorCallbackHandler()
    chat_model = ChatOllama(
        model=LLM_MODEL_NAME,
        streaming=True,
        verbose=True,
        callbacks=[callback],
    )

    task = asyncio.create_task(
        chat_model.ainvoke(input = messages)
    )

    try:
        async for token in callback.aiter():
            yield token
    except Exception as e:
        print(f"Caught exception: {e}")
    finally:
        callback.done.set()

    await task