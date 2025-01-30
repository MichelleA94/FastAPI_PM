from fastapi import Response, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from typing import Optional

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/instances",
    tags=["Instances"]
    )

@router.get("/", response_model=List[schemas.InstanceResponse])
def get_instances(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 100, skip: int = 0):
    if "admin" in current_user.username:
        instances = db.query(models.Instance).limit(limit).offset(skip).all()
    else:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    return instances

@router.get("/{id}", response_model=schemas.InstanceResponse)
def get_instance(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    instance = db.query(models.Instance).filter(models.Instance.id == id).first()
    if not instance:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                           detail = f"instance with id: {id} was not found")
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    return instance

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.InstanceResponse)
def create_instances(payload: schemas.InstanceCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_instance = models.Instance(**payload.dict())
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    db.add(new_instance)
    db.commit()
    db.refresh(new_instance)
    return new_instance

@router.put("/{id}", status_code = status.HTTP_201_CREATED, response_model=schemas.InstanceResponse)
def update_instance(id: int, payload: schemas.InstanceCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    instance_query = db.query(models.Instance).filter(models.Instance.id == id)
    instance = instance_query.first()
    if instance == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"instance with id: {id} was not found") # put you have to write all the fields / patch you only need to write the changed variable
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    instance_query.update(payload.dict())
    db.commit()
    return instance_query.first()

@router.delete("/{id}", status_code = status.HTTP_404_NOT_FOUND, response_model=schemas.InstanceResponse)
def delete_instance(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    instance_query = db.query(models.Instance).filter(models.Instance.id == id)
    instance = instance_query.first()
    if instance == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"instance with id: {id} was not found")
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    instance_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
