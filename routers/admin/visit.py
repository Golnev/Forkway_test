from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

import database
from models import models
from schemas import admin

router = APIRouter(
    prefix='/visit',
    tags=['Admin: Visit']
)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=admin.ShowVisit)
def create_visit(request: admin.Visit, db: Session = Depends(database.get_db)):
    new_visit = models.Visit(
        performer_id=request.performer_id,
        order_id=request.order_id,
        author_id=request.author_id,
        where_to_id=request.where_to_id,
    )
    db.add(new_visit)
    db.commit()
    db.refresh(new_visit)
    return new_visit


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=admin.ShowVisit)
def update_visit(id: int, request: admin.Visit, db: Session = Depends(database.get_db)):
    visit = db.query(models.Visit).filter(models.Visit.id == id)
    if not visit.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Visit with ID {id} is not found')
    visit.update(request.model_dump())
    db.commit()
    return visit.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_visit(id: int, db: Session = Depends(database.get_db)):
    visit = db.query(models.Visit).filter(models.Visit.id == id)
    if not visit.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Visit with ID {id} is not found')
    visit.delete(synchronize_session=False)
    db.commit()


@router.get('/visit_by_employee/{employee}', response_model=list[admin.ShowVisit])
def get_visit_by_employee(employee: str, offset: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    visit = (db.query(models.Visit).join(models.Employee).filter(models.Employee.name == employee)
             .offset(offset).limit(limit))
    if not visit.first():
        visit = (db.query(models.Visit).join(models.Employee).filter(models.Employee.username == employee)
                 .offset(offset).limit(limit))
        if not visit.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Visit with employee name {employee} is not found')
        return visit.all()
    return visit.all()


@router.get('/visit_by_outlet/{outlet}', response_model=list[admin.ShowVisit])
def get_visit_by_outlet(outlet: str, offset: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    visit = (db.query(models.Visit).join(models.Outlet).filter(models.Outlet.name == outlet)
             .offset(offset).limit(limit))
    if not visit.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Visit with outlet name {outlet} is '
                                                                          f'not found')
    return visit.all()
