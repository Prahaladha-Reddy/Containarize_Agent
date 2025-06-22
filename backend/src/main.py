from fastapi import FastAPI
import os
from api.db import init_db
from contextlib import asynccontextmanager
from api.chat.routing import router as chat_router


MY_PROJECT_NAME=os.getenv("MY_PROJECT_NAME")
MY_APP=os.getenv("MY_APP")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield



app = FastAPI(lifespan=lifespan)
app.include_router(chat_router,prefix="/chat")
@app.get("/")
def read_root():
    return {"Hello": "World again", "MY_PROJECT_NAME": MY_PROJECT_NAME, "MY_APP": MY_APP}
