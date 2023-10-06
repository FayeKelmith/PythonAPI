from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schema, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List

router = APIRouter(prefix="/posts", tags=['Posts'],)


@router.get("/", response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

# ROUTE TO CREATE POST
# NOTE: we didn't include the id in the schema because the id is useful only to the backend, the user need not hassle with identification, hence the creation of identity


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    # since we cannot return the submitted querry like we did with traditional sql, we use this technique that refreshes our variable and chagnges it's values.
    db.refresh(new_post)
    return new_post


# ROUTE TO GET THE LATEST POST
@router.get("/latest", response_model=schema.Post)
def get_latest_post(db: Session = Depends(get_db)):

    latest_post = db.query(models.Post).order_by(desc(models.Post.id)).first()
    return latest_post

# ROUTE TO RETURN A PARTICULAR POST BASED ON ID


@router.get("/{id}", response_model=schema.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "You sure that id exist?"}
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # deleting post
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schema.Post)
def update_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post_to_update = post_query.first()

    if post_to_update == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="We didn't find the post you want to update")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
