from fastapi import Response, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from typing import Optional

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
    )

@router.get("/", response_model=List[schemas.CustomerResponse])
def get_customers(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 100, skip: int = 0):
    if "admin" in current_user.role:
        customers = db.query(models.Customer).limit(limit).offset(skip).all()
    else:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    return customers

@router.get("/{id}", response_model=schemas.CustomerResponse)
def get_customer(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    customer = db.query(models.Customer).filter(models.Customer.id == id).first()
    if not customer:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                           detail = f"customer with id: {id} was not found")
    if "admin" not in current_user.role:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    return customer

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.CustomerResponse)
def create_customers(payload: schemas.CustomerCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_customer = models.Customer(**payload.dict())
    if "admin" not in current_user.role:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@router.put("/{id}", status_code = status.HTTP_201_CREATED, response_model=schemas.CustomerResponse)
def update_customer(id: int, payload: schemas.CustomerCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    customer_query = db.query(models.Customer).filter(models.Customer.id == id)
    customer = customer_query.first()
    if customer == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"customer with id: {id} was not found") # put you have to write all the fields / patch you only need to write the changed variable
    if "admin" not in current_user.role:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    customer_query.update(payload.dict())
    db.commit()
    return customer_query.first()

@router.delete("/{id}", status_code = status.HTTP_404_NOT_FOUND, response_model=schemas.CustomerResponse)
def delete_customer(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    customer_query = db.query(models.Customer).filter(models.Customer.id == id)
    customer = customer_query.first()
    if customer == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"customer with id: {id} was not found")
    if "admin" not in current_user.role:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform requested action")
    customer_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
