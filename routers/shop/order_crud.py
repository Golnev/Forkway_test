from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

import database
from models import models
from schemas import shop

router = APIRouter(
    prefix='/order',
    tags=['Shop: Order CRUD']
)


@router.get('_{phone_number}', response_model=list[shop.ShowOrder])
def get_orders(phone_number: str, offset: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    valid_phones = db.query(models.Customer).filter(models.Customer.phone == phone_number)
    if not valid_phones.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Access by phone number {phone_number} is forbidden')

    order = db.query(models.Order).order_by(models.Order.ended_at).offset(offset).limit(limit).all()
    return order


@router.post('_{phone_number}', status_code=status.HTTP_201_CREATED, response_model=shop.ShowOrder)
def create_order(phone_number: str, request: shop.CreateOrder, db: Session = Depends(database.get_db)):
    valid_phones = db.query(models.Customer).filter(models.Customer.phone == phone_number)
    if not valid_phones.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Access by phone number {phone_number} is forbidden')

    cust_outlets = [cust.outlet_id for cust in valid_phones.all()]
    if request.where_to_id not in cust_outlets:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{request.where_to_id} is not your outlet')

    employee_query = db.query(models.Employee).filter(models.Employee.id == request.performer_id).first()
    if not employee_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The employee with ID {request.where_to_id} does not exist')

    if request.where_to_id != employee_query.outlet_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'{request.performer_id} is not your employee')

    new_order = models.Order(
        ended_at=request.ended_at,
        where_to_id=request.where_to_id,
        author_id=valid_phones.first().id,
        status='started',
        performer_id=request.performer_id
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@router.put('_{phone_number}_{id}', status_code=status.HTTP_202_ACCEPTED, response_model=shop.ShowOrder)
def update_order(phone_number: str, id: int, request: shop.CreateOrder, db: Session = Depends(database.get_db)):
    customers = db.query(models.Customer).filter(models.Customer.phone == phone_number)
    if not customers.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Access by phone number {phone_number} is forbidden')

    customers_id = [customer.id for customer in customers.all()]

    order = db.query(models.Order).filter(models.Order.id == id)
    if not order.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Order with ID {id} is not found')

    if order.first().author_id not in customers_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{id} is not your outlet')

    employee_query = db.query(models.Employee).filter(models.Employee.id == request.performer_id).first()
    if not employee_query:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'The employee with ID {request.where_to_id} does not exist')

    if request.where_to_id != employee_query.outlet_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'{request.performer_id} is not your employee')

    cust_outlets = [cust.outlet_id for cust in customers.all()]
    if request.where_to_id not in cust_outlets:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{request.where_to_id} is not your outlet')

    order.update(request.model_dump())
    db.commit()
    return order.first()


@router.delete('_{phone_number}_{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_order(phone_number: str, id: int, db: Session = Depends(database.get_db)):
    customers = db.query(models.Customer).filter(models.Customer.phone == phone_number)
    if not customers.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Access by phone number {phone_number} is forbidden')

    customers_id = [customer.id for customer in customers.all()]

    order = db.query(models.Order).filter(models.Order.id == id)
    if not order.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Order with ID {id} is not found')

    if order.first().author_id not in customers_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{id} is not your outlet')

    order.delete(synchronize_session=False)
    db.commit()
