from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import Optional
from typing import List

#import database and models function
from ..database import get_db
from .. import models, schemas, OAuth2


# Initialize FastAPI application
router = APIRouter(
                tags=['Posts']
                )


@router.get("/")
def read_root():
    return {"Hello": "My API"}

# Function to get posts
@router.get("/posts", response_model=List[schemas.Post])
def find_posts(db: Session = Depends(get_db), user_id: int = 
                 Depends(OAuth2.get_current_user)):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")
                     ).outerjoin(models.Vote, models.Vote.post_id == models.Post.post_id
                                 ).group_by(models.Post.post_id).all()

    # Map the results correctly: each row is (Post, votes)
    result = []
    for post, vote_count in posts:
        post.votes = vote_count  # Add the vote count to the post object
        result.append(post)

    return result


# Function to post a single post
@router.post("/posts", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostBase, db: Session = Depends(get_db), current_user = 
                 Depends(OAuth2.get_current_user)):
    
    # Create a new Post instance
    new_post = models.Post(user_id=current_user.user_id, **post.model_dump())
    # Add the new post to the database session
    db.add(new_post)
    db.commit()  # Commit the transaction to save the post
    db.refresh(new_post)  # Refresh the instance to get the updated data from the database
    return new_post


@router.get("/posts/{id}", response_model=schemas.Post)
def read_post(id:int, db: Session = Depends(get_db), current_user = Depends(OAuth2.get_current_user)):
    post_with_vote = db.query(models.Post, func.count(models.Vote.post_id).label("votes")
                              ).outerjoin(models.Vote, models.Vote.post_id == models.Post.post_id
                                          ).filter(models.Post.post_id == id).group_by(models.Post.post_id).first()

    if not post_with_vote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")

    # Unpack the result: it returns a tuple (PostObject, vote_count)
    post, vote_count = post_with_vote
    post.votes = vote_count

    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user = Depends(OAuth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.post_id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    # Check if the post belongs to the current user
    if post.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to delete this post")
    db.delete(post)  # Delete the post from the database
    db.commit() 
    return


 # Function to update a post
@router.put("/posts/{id}", response_model=schemas.Post)
def update_post(id:int, post: schemas.PostBase, db: Session = Depends(get_db), current_user = Depends(OAuth2.get_current_user)):
    # Check if the post exists              
    existing_post = db.query(models.Post).filter(models.Post.post_id == id).first()
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} was not found")
    # Check if the post belongs to the current user
    if existing_post.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to update this post")
    # Update the post with the new data
    existing_post.title = post.title
    existing_post.content = post.content
    existing_post.published = post.published
    db.commit()
    db.refresh(existing_post)  # Refresh the instance to get the updated data from the database
    return existing_post
