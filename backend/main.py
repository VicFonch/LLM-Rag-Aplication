#uvicorn main:app --reload

from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from functions.database import streaming_response
from functions.model import Message

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    #allow_origins=["http://localhost:5173/"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Post bot response
@app.post("/api/similarity-search")
async def get_similarity_search(message: Message):
    try:
        generator = streaming_response(message.query, message.chat_history_json_path)
        return  StreamingResponse(generator, media_type="text/event-stream")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error during similarity search: {e}")

