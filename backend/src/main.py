from fastapi import FastAPI
import os
app = FastAPI()
MY_PROJECT_NAME=os.getenv("MY_PROJECT_NAME")
MY_APP=os.getenv("MY_APP")
@app.get("/")
def read_root():
    return {"Hello": "World again", "MY_PROJECT_NAME": MY_PROJECT_NAME, "MY_APP": MY_APP}
