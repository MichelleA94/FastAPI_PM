from fastapi import Response, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from typing import Optional

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/modalities",
    tags=["Modalities"]
    )

@router.get("/", response_model=List[schemas.ModalityResponse])
def get_modalities(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 100, skip: int = 0):
    if "admin" in current_user.username:
        modalities = db.query(models.Modality).limit(limit).offset(skip).all()
    else:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    return modalities

@router.get("/{id}", response_model=schemas.ModalityResponse)
def get_modality(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    modality = db.query(models.Modality).filter(models.Modality.id == id).first()
    if not modality:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                           detail = f"modality with id: {id} was not found")
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    return modality

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.ModalityResponse)
def create_modalities(payload: schemas.ModalitytCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_modality = models.Modality(**payload.dict())
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    db.add(new_modality)
    db.commit()
    db.refresh(new_modality)
    return new_modality

@router.put("/{id}", status_code = status.HTTP_201_CREATED, response_model=schemas.ModalityResponse)
def update_modality(id: int, payload: schemas.ModalitytCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    modality_query = db.query(models.Modality).filter(models.Modality.id == id)
    modality = modality_query.first()
    if modality == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"modality with id: {id} was not found") # put you have to write all the fields / patch you only need to write the changed variable
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    modality_query.update(payload.dict())
    db.commit()
    return modality_query.first()

@router.delete("/{id}", status_code = status.HTTP_404_NOT_FOUND, response_model=schemas.ModalityResponse)
def delete_modality(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    modality_query = db.query(models.Modality).filter(models.Modality.id == id)
    modality = modality_query.first()
    if modality == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"modality with id: {id} was not found")
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    modality_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
