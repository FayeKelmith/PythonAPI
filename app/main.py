from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schema, utils
from .database import engine
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .routers import post, user, auth
app = FastAPI()

# TO create the database using the models imported and the engine created.

# hashing algorithm

models.Base.metadata.create_all(bind=engine)


# INFO: we have to write
while True:
    try:
        conn = psycopg2.connect(
            host='localhost', database='pythonapi', user='postgres', password='pythonapi123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("We got to the database")
        break

    except Exception as error:
        print(f'We ran into an error {error}')

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"Message": "Hello world"}
