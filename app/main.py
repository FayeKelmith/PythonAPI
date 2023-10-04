from fastapi import FastAPI,Response,status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

#we define a class to create a schema 
class Post(BaseModel):
    title: str
    content: str
    #we can give default value that is an optinal value
    published: bool = True
    
    rating: Optional[int] = None
    

#An array to store the posts
my_post = [{"title": "title of post 1", "content": "content of post1", "id":1},{"tittle": "favorite foods", "content": "I like pizza", "id":2}]

#primitive way of finding the post, not recommended since we'll use a database later.
def find_post(id):
    for p in my_post:
        if p["id"]==id:
            return p
        
#primitive way of deleting, we'll use a database later
def find_post_index(id):
    for index, p in enumerate(my_post):
        if p['id'] == id:
            return index

# ROUTE
@app.get("/")
def root():
    return {"Message": "Hello world"}


#ROUTE TO GET POSTS
@app.get("/posts")
def get_posts():
    return {"data":my_post}

#ROUTE TO CREATE POST
#NOTE: we didn't include the id in the schema because the id is useful only to the backend, the user need not hassle with identification, hence the creation of identity
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0,1000)
    my_post.append(post_dict)
    return {"data": my_post}


#ROUTE TO GET THE LATEST POST
@app.get("/posts/latest")
def get_latest_post():
    post = my_post[-1]
    return {"latest": post}

#ROUTE TO RETURN A PARTICULAR POST BASED ON ID
@app.get("/posts/{id}")
#we define the data type to make sure that the id is alwasy converted else it will come as a string
def get_post(id: int, response: Response):
    post = find_post(id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id: {id} was not found')
    
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "You sure that id exist?"}
    return {"Here is post": post}

@app.delete("/posts/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #deleting post
    #find index in array with specific array
    index = find_post_index(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    #fetch the post to be updated and make update
    index = find_post_index(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="We didn't find the post you want to update")
    
    post_dict = post.dict()
    #adding the id to the payload
    post_dict['id'] = id
    
    my_post[index] = post_dict
    
    print(post)
    return {"message": f"Updated a post : {post_dict}"}