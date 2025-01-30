from fastapi import Response, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from typing import Optional

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/scripts",
    tags=["Scripts"]
    )

@router.get("/", response_model=List[schemas.SriptResponse])
def get_scripts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 100, skip: int = 0):
    if "admin" in current_user.username:
        scripts = db.query(models.Script).limit(limit).offset(skip).all()
    else:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    return scripts

@router.get("/{id}", response_model=schemas.SriptResponse)
def get_script(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    script = db.query(models.Script).filter(models.Script.id == id).first()
    if not script:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                           detail = f"script with id: {id} was not found")
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    return script

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.SriptResponse)
def create_scripts(payload: schemas.SriptCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_script = models.Script(**payload.dict())
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    db.add(new_script)
    db.commit()
    db.refresh(new_script)
    return new_script

@router.put("/{id}", status_code = status.HTTP_201_CREATED, response_model=schemas.SriptResponse)
def update_script(id: int, payload: schemas.SriptCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    script_query = db.query(models.Script).filter(models.Script.id == id)
    script = script_query.first()
    if script == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"script with id: {id} was not found") # put you have to write all the fields / patch you only need to write the changed variable
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    script_query.update(payload.dict())
    db.commit()
    return script_query.first()

@router.delete("/{id}", status_code = status.HTTP_404_NOT_FOUND, response_model=schemas.SriptResponse)
def delete_script(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    script_query = db.query(models.Script).filter(models.Script.id == id)
    script = script_query.first()
    if script == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"script with id: {id} was not found")
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    script_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
