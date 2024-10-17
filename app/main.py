from typing import Union
from fastapi import FastAPI
from routes.user import router as user_router
from db.db import create_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_tables()

app.include_router(user_router)

@app.get("/")
def read_root():
    return {"Hello": "Worldaaaaaaaaaaaaaaaaa"}

