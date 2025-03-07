from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/login",
    tags=['Authentication']
    )

@router.post('/', response_model=schemas.Token)
def login(payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == payload.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                           detail = f"Invalid Credentials")
    if not utils.verify(payload.password, user.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                           detail = f"Invalid Credentials")
    # create a token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}