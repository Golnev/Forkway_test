from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

import database
from models import models
from schemas import admin

router = APIRouter(
    prefix='/customer',
    tags=['Admin: Customer']
)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=admin.ShowCustomer)
def create_customer(request: admin.Customer, db: Session = Depends(database.get_db)):
    new_customer = models.Customer(
        name=request.name,
        phone=request.phone,
        outlet_id=request.outlet_id
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=admin.ShowCustomer)
def update_customer(id: int, request: admin.Customer, db: Session = Depends(database.get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == id)
    if not customer.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Customer with ID {id} is not found')
    customer.update(request.model_dump())
    db.commit()
    return customer.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(id: int, db: Session = Depends(database.get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == id)
    if not customer.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Customer with ID {id} is not found')
    customer.delete(synchronize_session=False)
    db.commit()


@router.get('/customer_by_outlet/{outlet}', response_model=list[admin.ShowCustomer])
def get_customer_by_outlet(outlet: str, db: Session = Depends(database.get_db)):
    customer = db.query(models.Customer).join(models.Outlet).filter(models.Outlet.name == outlet)
    if not customer.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Customer with outlet name {outlet} is '
                                                                          f'not found')
    return customer.all()
