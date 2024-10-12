from typing import Union
from fastapi import FastAPI
from routes.user import router as user_router

app = FastAPI()

app.include_router(user_router)

@app.get("/")
def read_root():
    return {"Hello": "Worldaaaaaaaaaaaaaaaaa"}

