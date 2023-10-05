from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import desc
app = FastAPI()

# TO create the database using the models imported and the engine created.
models.Base.metadata.create_all(bind=engine)


# we define a class to create a schema


class Post(BaseModel):
    title: str
    content: str
    published: bool = False


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


@app.get("/")
def root():
    return {"Message": "Hello world"}


# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     # db.querry(models.Post) return just a sql querry. The returned querry is then synthesized by appended methods like .all()
#     posts = db.query(models.Post).all()
#     print(posts)
#     return {"status": "yehp"}
# ROUTE TO GET POSTS


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}

# ROUTE TO CREATE POST
# NOTE: we didn't include the id in the schema because the id is useful only to the backend, the user need not hassle with identification, hence the creation of identity


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # # we do it this way to prevent SQL injections
    # cursor.execute("""INSERT INTO posts(title, content,published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # # to actually save the values into the table.
    # conn.commit()

    # NOTE: we unpack post.
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    # since we cannot return the submitted querry like we did with traditional sql, we use this technique that refreshes our variable and chagnges it's values.
    db.refresh(new_post)
    return {"data": new_post}


# ROUTE TO GET THE LATEST POST
@app.get("/posts/latest")
def get_latest_post(db: Session = Depends(get_db)):

    latest_post = db.query(models.Post).order_by(desc(models.Post.id)).first()
    return {"latest": latest_post}

# ROUTE TO RETURN A PARTICULAR POST BASED ON ID


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.querry(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "You sure that id exist?"}
    return {"Here is post": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # deleting post
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post_to_update = post_query.first()

    if post_to_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="We didn't find the post you want to update")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"updated post: ": post_query.first()}
