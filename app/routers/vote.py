from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, OAuth2
from ..database import get_db

# Initialize FastAPI router
router = APIRouter(
            tags=['Votes']
        )
# Function to create a vote
@router.post("/vote", status_code=status.HTTP_201_CREATED)
def vote_post(vote: schemas.Vote, db: Session = Depends(get_db), current_user = Depends(OAuth2.get_current_user)):
    # Check if the post exists
    post = db.query(models.Post).filter(models.Post.post_id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found")
    
    # Check if the user has already voted on this post
    existing_vote = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.user_id
    ).first()
    
    if vote.dir == 1:  # User is voting for the post
        if existing_vote:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="You have already voted on this post")
        new_vote = models.Vote(user_id=current_user.user_id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}
    
    elif vote.dir == 0:  # User is un-voting for the post
        if not existing_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Vote not found")
        db.delete(existing_vote)
        db.commit()
        return {"message": "Vote removed successfully"}
    
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid vote direction")