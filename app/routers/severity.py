from fastapi import Response, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from typing import Optional

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/severities",
    tags=["Severities"]
    )

@router.get("/", response_model=List[schemas.SeverityResponse])
def get_severities(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 100, skip: int = 0):
    if "admin" in current_user.role:
        severities = db.query(models.Severity).limit(limit).offset(skip).all()
    else:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    return severities

@router.get("/{id}", response_model=schemas.SeverityResponse)
def get_severity(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    severity = db.query(models.Severity).filter(models.Severity.id == id).first()
    if not severity:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                           detail = f"severity with id: {id} was not found")
    if "admin" not in current_user.role:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    return severity

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.SeverityResponse)
def create_severitiess(payload: schemas.SeverityCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_severity = models.Severity(**payload.dict())
    if "admin" not in current_user.role:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    db.add(new_severity)
    db.commit()
    db.refresh(new_severity)
    return new_severity

@router.put("/{id}", status_code = status.HTTP_201_CREATED, response_model=schemas.SeverityResponse)
def update_severity(id: int, payload: schemas.SeverityCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    severity_query = db.query(models.Severity).filter(models.Severity.id == id)
    severity = severity_query.first()
    if severity == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"severity with id: {id} was not found") # put you have to write all the fields / patch you only need to write the changed variable
    if "admin" not in current_user.role:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    severity_query.update(payload.dict())
    db.commit()
    return severity_query.first()

@router.delete("/{id}", status_code = status.HTTP_404_NOT_FOUND, response_model=schemas.SeverityResponse)
def delete_severity(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    severity_query = db.query(models.Severity).filter(models.Severity.id == id)
    severity = severity_query.first()
    if severity == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"severity with id: {id} was not found")
    if "admin" not in current_user.role:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    severity_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
