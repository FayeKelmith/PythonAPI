from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
app = FastAPI()

# we define a class to create a schema

# NOTE: pythonapi password : 'pythonapi123'


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


# An array to store the posts
my_post = [{"title": "title of post 1", "content": "content of post1", "id": 1}, {
    "tittle": "favorite foods", "content": "I like pizza", "id": 2}]

# primitive way of finding the post, not recommended since we'll use a database later.


def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p

# primitive way of deleting, we'll use a database later


def find_post_index(id):
    for index, p in enumerate(my_post):
        if p['id'] == id:
            return index

# ROUTE


@app.get("/")
def root():
    return {"Message": "Hello world"}


# ROUTE TO GET POSTS
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

# ROUTE TO CREATE POST
# NOTE: we didn't include the id in the schema because the id is useful only to the backend, the user need not hassle with identification, hence the creation of identity


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # we do it this way to prevent SQL injections
    cursor.execute("""INSERT INTO posts(title, content,published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()

    # to actually save the values into the table.
    conn.commit()
    return {"data": new_post}


# ROUTE TO GET THE LATEST POST
@app.get("/posts/latest")
def get_latest_post():
    post = my_post[-1]
    return {"latest": post}

# ROUTE TO RETURN A PARTICULAR POST BASED ON ID


@app.get("/posts/{id}")
# we define the data type to make sure that the id is alwasy converted else it will come as a string
def get_post(id: int):
    cursor.execute('''SELECT * from posts where id = %s''', (str(id)))

    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "You sure that id exist?"}
    return {"Here is post": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    cursor.execute(
        """DELETE from posts where id = %s RETURNING *""", str(id),)

    deleted_post = cursor.fetchone()

    conn.commit()
    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        '''Update posts set title=%s, content = %s, published = %s where id = %s returning *''', (post.title, post.content, post.published, str(id)))

    updated_post = cursor.fetchone()

    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="We didn't find the post you want to update")

    return {"updated post: ": updated_post}
