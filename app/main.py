from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from .database import engine
from .routers import post, user, auth, vote
app = FastAPI()

# if it is meant only for a set of people with specific domain properties, maybe a network.
origins = ["*"]
[
    "https://www.google.com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)
# used to lad our database using sqlalchemy
# models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"Message": "Hello world"}
