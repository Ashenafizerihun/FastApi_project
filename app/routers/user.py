from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

# Initialize FastAPI router
router = APIRouter(
            tags=['Users']
        )

# Function to create a user credential
@router.post("/user", status_code = status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # Check if the user already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already registered")
    # Hash the password
    hashed_password = utils.hash_password(user.password)
    # Create a new User instance with the hashed password
    user.password = hashed_password

    # Create a new Post instance
    new_user = models.User(**user.model_dump())
    # Add the new post to the database session
    db.add(new_user)
    db.commit()  # Commit the transaction to save the post
    db.refresh(new_user)  # Refresh the instance to get the updated data from the database
    return new_user