from fastapi import FastAPI
from . import models, config
from .database import engine
from .routers import post, user, auth
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"Message": "Hello world"}
