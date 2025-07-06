from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schemas, database, utils, OAuth2


# Initialize FastAPI router
router = APIRouter(
            tags=['User_Authentication']
        )

# Function to post a single post
@router.post("/login", response_model=schemas.Token)
def user_login(user_credential:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credential")
    if not utils.verify_password(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credential")
    #create token
    access_token = OAuth2.create_access_token(data={"user_id": user.user_id})
    #return token
    return {"access_token": access_token, "token_type": "bearer"}




