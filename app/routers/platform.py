from fastapi import Response, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from typing import Optional

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/platforms",
    tags=["Platforms"]
    )

@router.get("/", response_model=List[schemas.PlatformResponse])
def get_platforms(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 100, skip: int = 0):
    if "admin" in current_user.role:
        platforms = db.query(models.Platform).limit(limit).offset(skip).all()
    else:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    return platforms

@router.get("/{id}", response_model=schemas.PlatformResponse)
def get_platform(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    platform = db.query(models.Platform).filter(models.Platform.id == id).first()
    if not platform:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                           detail = f"platform with id: {id} was not found")
    if "admin" not in current_user.role:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    return platform

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.PlatformResponse)
def create_platforms(payload: schemas.PlatformCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_platform = models.Platform(**payload.dict())
    if "admin" not in current_user.role:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    db.add(new_platform)
    db.commit()
    db.refresh(new_platform)
    return new_platform

@router.put("/{id}", status_code = status.HTTP_201_CREATED, response_model=schemas.PlatformResponse)
def update_platform(id: int, payload: schemas.PlatformCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    platform_query = db.query(models.Platform).filter(models.Platform.id == id)
    platform = platform_query.first()
    if platform == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"platform with id: {id} was not found") # put you have to write all the fields / patch you only need to write the changed variable
    if "admin" not in current_user.role:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    platform_query.update(payload.dict())
    db.commit()
    return platform_query.first()

@router.delete("/{id}", status_code = status.HTTP_404_NOT_FOUND, response_model=schemas.PlatformResponse)
def delete_platform(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    platform_query = db.query(models.Platform).filter(models.Platform.id == id)
    platform = platform_query.first()
    if platform == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"platform with id: {id} was not found")
    if "admin" not in current_user.role:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    platform_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
