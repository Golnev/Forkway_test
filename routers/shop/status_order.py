from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

import database
from models import models
from schemas import admin, shop

router = APIRouter(
    prefix='/status_order',
    tags=['Shop: Change order status']
)


@router.put('/{phone_number}_{id}', status_code=status.HTTP_202_ACCEPTED, response_model=shop.ShowOrder)
def update_order_status(phone_number: str, id: int, request: admin.OrderStatus, db: Session = Depends(database.get_db)):
    valid_phones = db.query(models.Employee).filter(models.Employee.username == phone_number)
    if not valid_phones.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Access by phone number {phone_number} is forbidden')

    valid_status = ['started', 'ended', 'in process', 'awaiting', 'canceled']
    if request.status not in valid_status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Status {request.status} is not allowed')

    order = db.query(models.Order).filter(models.Order.id == id)
    if not order.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Outlet with ID {id} is not found')
    order.update(request.model_dump())
    db.commit()
    return order.first()
