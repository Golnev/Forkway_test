from datetime import datetime, timezone

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

import database
from models import models
from schemas import shop

router = APIRouter(
    prefix='/visit',
    tags=['Shop: Visit CRUD']
)


@router.get('_{phone_number}', response_model=list[shop.ShowVisit])
def get_visits(phone_number: str, offset: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    valid_phones = db.query(models.Customer).filter(models.Customer.phone == phone_number)
    if not valid_phones.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Access by phone number {phone_number} is forbidden')

    visits = db.query(models.Visit).order_by(models.Visit.created_at).offset(offset).limit(limit).all()
    return visits


@router.post('_{phone_number}', status_code=status.HTTP_201_CREATED, response_model=shop.ShowVisit)
def create_visit(phone_number: str, request: shop.CreateVisit, db: Session = Depends(database.get_db)):
    #  Verification of the customer's phone number.
    customers = db.query(models.Customer).filter(models.Customer.phone == phone_number)
    if not customers.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Access by phone number {phone_number} is forbidden')
    customers_id = [customer.id for customer in customers.all()]

    # Order verification
    order = db.query(models.Order).filter(models.Order.id == request.order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The order with ID {request.order_id} does not exist')
    if order.author_id not in customers_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'{order.id} is not your order')

    visit = db.query(models.Visit).filter(models.Visit.order_id == request.order_id)
    if visit.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'The order with ID {request.order_id} already in visit')

    if datetime.now(timezone.utc) > order.ended_at:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'The order ID {request.order_id} has expired')

    # Employee verification
    if request.performer_id != order.performer_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Employee with ID {request.performer_id} '
                                   f'does not apply to order ID {request.order_id}')

    # Outlet verification
    if request.where_to_id != order.where_to_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Outlet with ID {request.where_to_id} '
                                   f'does not apply to order ID {request.order_id}')

    new_visit = models.Visit(
        performer_id=request.performer_id,
        order_id=request.order_id,
        author_id=customers_id[0],
        where_to_id=request.where_to_id
    )
    db.add(new_visit)
    db.commit()
    db.refresh(new_visit)
    return new_visit


@router.put('_{phone_number}_{id}', status_code=status.HTTP_202_ACCEPTED, response_model=shop.ShowVisit)
def update_visit(phone_number: str, id: int, request: shop.CreateVisit, db: Session = Depends(database.get_db)):
    #  Verification of the customer's phone number.
    customers = db.query(models.Customer).filter(models.Customer.phone == phone_number)
    if not customers.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Access by phone number {phone_number} is forbidden')
    customers_id = [customer.id for customer in customers.all()]

    visit = db.query(models.Visit).filter(models.Visit.id == id)

    # Order verification
    order = db.query(models.Order).filter(models.Order.id == request.order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The order with ID {request.order_id} does not exist')
    if order.author_id not in customers_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'{request.order.id} is not your order')

    if datetime.now(timezone.utc) > order.ended_at:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'The order ID {request.order_id} has expired')

    # Employee verification
    if request.performer_id != order.performer_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Employee with ID {request.performer_id} '
                                   f'does not apply to order ID {request.order_id}')

    # Outlet verification
    if request.where_to_id != order.where_to_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Outlet with ID {request.where_to_id} '
                                   f'does not apply to order ID {request.order_id}')

    visit.update(request.model_dump())
    db.commit()
    return visit.first()


@router.delete('_{phone_number}_{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_visit(phone_number: str, id: int, db: Session = Depends(database.get_db)):
    customers = db.query(models.Customer).filter(models.Customer.phone == phone_number)
    if not customers.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Access by phone number {phone_number} is forbidden')
    customers_id = [customer.id for customer in customers.all()]

    visit = db.query(models.Visit).filter(models.Visit.id == id)
    if not visit.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Visit with ID {id} is not found')

    if visit.first().author_id not in customers_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'The visit with ID {id} is not yours')

    visit.delete(synchronize_session=False)
    db.commit()
