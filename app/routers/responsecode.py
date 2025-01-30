from fastapi import Response, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from typing import Optional

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/responsecodes",
    tags=["Response Codes"]
    )

@router.get("/", response_model=List[schemas.ResponseCodeResponse])
def get_responsecodes(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 100, skip: int = 0):
    if "admin" in current_user.username:
        responsecodes = db.query(models.ResponseCode).limit(limit).offset(skip).all()
    else:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    return responsecodes

@router.get("/{id}", response_model=schemas.ResponseCodeResponse)
def get_responsecode(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    responsecode = db.query(models.ResponseCode).filter(models.ResponseCode.id == id).first()
    if not responsecode:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                           detail = f"responsecode with id: {id} was not found")
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    return responsecode

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.ResponseCodeResponse)
def create_responsecodes(payload: schemas.ResponseCodeCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_responsecode = models.ResponseCode(**payload.dict())
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    db.add(new_responsecode)
    db.commit()
    db.refresh(new_responsecode)
    return new_responsecode

@router.put("/{id}", status_code = status.HTTP_201_CREATED, response_model=schemas.ResponseCodeResponse)
def update_responsecode(id: int, payload: schemas.ResponseCodeCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    responsecode_query = db.query(models.ResponseCode).filter(models.ResponseCode.id == id)
    responsecode = responsecode_query.first()
    if responsecode == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"responsecode with id: {id} was not found") # put you have to write all the fields / patch you only need to write the changed variable
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    responsecode_query.update(payload.dict())
    db.commit()
    return responsecode_query.first()

@router.delete("/{id}", status_code = status.HTTP_404_NOT_FOUND, response_model=schemas.ResponseCodeResponse)
def delete_responsecode(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    responsecode_query = db.query(models.ResponseCode).filter(models.ResponseCode.id == id)
    responsecode = responsecode_query.first()
    if responsecode == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"responsecode with id: {id} was not found")
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    responsecode_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
