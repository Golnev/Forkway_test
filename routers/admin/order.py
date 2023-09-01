from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

import database
from models import models
from schemas import admin

router = APIRouter(
    prefix='/order',
    tags=['Admin: Order']
)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=admin.ShowOrder)
def create_order(request: admin.Order, db: Session = Depends(database.get_db)):
    valid_status = ['started', 'ended', 'in process', 'awaiting', 'canceled']
    if request.status not in valid_status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Status {request.status} is not allowed')

    new_order = models.Order(
        ended_at=request.ended_at,
        where_to_id=request.where_to_id,
        author_id=request.author_id,
        status=request.status,
        performer_id=request.performer_id
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=admin.ShowOrder)
def update_order(id: int, request: admin.Order, db: Session = Depends(database.get_db)):
    valid_status = ['started', 'ended', 'in process', 'awaiting', 'canceled']
    if request.status not in valid_status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Status {request.status} is not allowed')

    order = db.query(models.Order).filter(models.Order.id == id)
    if not order.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Outlet with ID {id} is not found')
    order.update(request.model_dump())
    db.commit()
    return order.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_order(id: int, db: Session = Depends(database.get_db)):
    order = db.query(models.Order).filter(models.Order.id == id)
    if not order.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Outlet with ID {id} is not found')
    order.delete(synchronize_session=False)
    db.commit()


@router.get('/order_by_employee/{employee}', response_model=list[admin.ShowOrder])
def get_order_by_employee(employee: str, offset: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    order = (db.query(models.Order).join(models.Employee).filter(models.Employee.name == employee)
             .offset(offset).limit(limit))
    if not order.first():
        order = (db.query(models.Order).join(models.Employee).filter(models.Employee.username == employee)
                 .offset(offset).limit(limit))
        if not order.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Order with employee name {employee} is not found')
        return order.all()
    return order.all()


@router.get('/order_by_outlet/{outlet}', response_model=list[admin.ShowOrder])
def get_order_by_outlet(outlet: str, offset: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    order = db.query(models.Order).join(models.Outlet).filter(models.Outlet.name == outlet).offset(offset).limit(limit)
    if not order.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Order with outlet name {outlet} is '
                                                                          f'not found')
    return order.all()
