#uvicorn main:app --reload

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from functions.llm_processing import streaming_response

from dbmodels import Message
from enviroment import FRONTEND_URL

from routes.crud_task import crud_task
from routes.security_task import security_task

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # allow_origins=[
    #     FRONTEND_URL + "/",
    #     FRONTEND_URL + "/login",
    # ],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crud_task)
app.include_router(security_task)

# Post bot response
@app.post("/api/striming_response")
async def post_striming_response(message: Message):
    try:
        generator = streaming_response(message.query, message.chat_history)
        return StreamingResponse(generator, media_type="text/event-stream")
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error during similarity search: {e}")

