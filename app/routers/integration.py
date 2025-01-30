from fastapi import Response, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from typing import Optional

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/integrations",
    tags=["Integrations"]
    )

@router.get("/", response_model=List[schemas.IntegrationResponse])
def get_integrations(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 100, skip: int = 0):
    if "admin" in current_user.username:
        integrations = db.query(models.Integration).limit(limit).offset(skip).all()
    else:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    return integrations

@router.get("/{id}", response_model=schemas.IntegrationResponse)
def get_integration(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    integration = db.query(models.Integration).filter(models.Integration.id == id).first()
    if not integration:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                           detail = f"integration with id: {id} was not found")
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    return integration

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.IntegrationResponse)
def create_integrations(payload: schemas.IntegrationCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_integration = models.Integration(**payload.dict())
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    db.add(new_integration)
    db.commit()
    db.refresh(new_integration)
    return new_integration

@router.put("/{id}", status_code = status.HTTP_201_CREATED, response_model=schemas.IntegrationResponse)
def update_integration(id: int, payload: schemas.IntegrationCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    integration_query = db.query(models.Integration).filter(models.Integration.id == id)
    integration = integration_query.first()
    if integration == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"integration with id: {id} was not found") # put you have to write all the fields / patch you only need to write the changed variable
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    integration_query.update(payload.dict())
    db.commit()
    return integration_query.first()

@router.delete("/{id}", status_code = status.HTTP_404_NOT_FOUND, response_model=schemas.IntegrationResponse)
def delete_integration(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    integration_query = db.query(models.Integration).filter(models.Integration.id == id)
    integration = integration_query.first()
    if integration == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"integration with id: {id} was not found")
    if "admin" not in current_user.username:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    integration_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
