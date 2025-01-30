from fastapi import Response, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from typing import Optional

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/queues",
    tags=["Queues"]
    )

@router.get("/", response_model=List[schemas.QueueResponse])
def get_queues(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 100, skip: int = 0):
    if "admin" in current_user.username:
        queues = db.query(models.Queue).limit(limit).offset(skip).all()
    else:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    return queues

@router.get("/{id}", response_model=schemas.QueueResponse)
def get_queue(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    queue = db.query(models.Queue).filter(models.Queue.id == id).first()
    if not queue:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                           detail = f"queue with id: {id} was not found")
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    return queue

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.QueueResponse)
def create_queues(payload: schemas.QueueCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_queue = models.Queue(**payload.dict())
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    db.add(new_queue)
    db.commit()
    db.refresh(new_queue)
    return new_queue

@router.put("/{id}", status_code = status.HTTP_201_CREATED, response_model=schemas.QueueResponse)
def update_queue(id: int, payload: schemas.QueueCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    queue_query = db.query(models.Queue).filter(models.Queue.id == id)
    queue = queue_query.first()
    if queue == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"queue with id: {id} was not found") # put you have to write all the fields / patch you only need to write the changed variable
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    queue_query.update(payload.dict())
    db.commit()
    return queue_query.first()

@router.delete("/{id}", status_code = status.HTTP_404_NOT_FOUND, response_model=schemas.QueueResponse)
def delete_queue(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    queue_query = db.query(models.Queue).filter(models.Queue.id == id)
    queue = queue_query.first()
    if queue == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"queue with id: {id} was not found")
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    queue_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
