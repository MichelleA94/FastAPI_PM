from fastapi import Response, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from typing import Optional

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/events",
    tags=["Events"]
    )

@router.get("/", response_model=List[schemas.EventResponse])
def get_events(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 100, skip: int = 0):
    if "admin" in current_user.role:
        events = db.query(models.Event).limit(limit).offset(skip).all()
    else:
        events = db.query(models.Event).filter(models.Event.owner_id == current_user.id).limit(limit).offset(skip).all()

    return events

@router.get("/{id}", response_model=schemas.EventResponse)
def get_event(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    event = db.query(models.Event).filter(models.Event.id == id).first()
    if not event:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                           detail = f"event with id: {id} was not found")

    if "admin" not in current_user.role:
        if event.owner_id != current_user.id:
            raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    return event

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.EventResponse)
def create_events(payload: schemas.EventCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_event = models.Event(owner_id=current_user.id, **payload.dict())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.put("/{id}", status_code = status.HTTP_201_CREATED, response_model=schemas.EventResponse)
def update_event(id: int, payload: schemas.EventCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    event_query = db.query(models.Event).filter(models.Event.id == id)
    event = event_query.first()
    if event == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"event with id: {id} was not found") # put you have to write all the fields / patch you only need to write the changed variable
    if "admin" not in current_user.role:
        if event.owner_id != current_user.id:
            raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    event_query.update(payload.dict())
    db.commit()
    return event_query.first()

@router.delete("/{id}", status_code = status.HTTP_404_NOT_FOUND, response_model=schemas.EventResponse)
def delete_event(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    event_query = db.query(models.Event).filter(models.Event.id == id)
    event = event_query.first()
    if event == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"event with id: {id} was not found")
    if "admin" not in current_user.role:
        if event.owner_id != current_user.id:
            raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    event_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# , search: Optional[str] = ""
#.filter(models.Event.title contains(search)) {{URL}}events?search=somthing%beaches