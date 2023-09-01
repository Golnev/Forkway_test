from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

import database
from models import models
from schemas import admin

router = APIRouter(
    prefix='/outlet',
    tags=['Admin: Outlet']
)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=admin.ShowOutlet)
def create_outlet(request: admin.Outlet, db: Session = Depends(database.get_db)):
    new_outlet = models.Outlet(
        name=request.name,
    )
    db.add(new_outlet)
    db.commit()
    db.refresh(new_outlet)
    return new_outlet


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=admin.ShowOutlet)
def update_outlet(id: int, request: admin.Outlet, db: Session = Depends(database.get_db)):
    outlet = db.query(models.Outlet).filter(models.Outlet.id == id)
    if not outlet.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Outlet with ID {id} is not found')
    outlet.update(request.model_dump())
    db.commit()
    return outlet.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_outlet(id: int, db: Session = Depends(database.get_db)):
    outlet = db.query(models.Outlet).filter(models.Outlet.id == id)
    if not outlet.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Outlet with ID {id} is not found')
    outlet.delete(synchronize_session=False)
    db.commit()


@router.get('/outlet_by_name/{name}', response_model=admin.ShowOutlet)
def get_outlet_by_name(name: str, db: Session = Depends(database.get_db)):
    outlet = db.query(models.Outlet).filter(models.Outlet.name == name)
    if not outlet.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Outlet with name {name} is not found')
    return outlet.first()


@router.get('/outlet_by_employee/{employee}', response_model=list[admin.ShowOutlet])
def get_outlet_by_employee(employee: str, offset: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    outlet = (db.query(models.Outlet).join(models.Employee).filter(models.Employee.name == employee)
              .offset(offset).limit(limit))
    if not outlet.first():
        outlet = (db.query(models.Outlet).join(models.Employee).filter(models.Employee.username == employee)
                  .offset(offset).limit(limit))
        if not outlet.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Outlet with employee name {employee} is not found')
        return outlet.all()
    return outlet.all()
