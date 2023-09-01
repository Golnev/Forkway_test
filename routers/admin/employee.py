from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

import database
from models import models
from schemas import admin

router = APIRouter(
    prefix='/employee',
    tags=['Admin: Employee']
)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=admin.ShowEmployee)
def create_employee(request: admin.Employee, db: Session = Depends(database.get_db)):
    new_employee = models.Employee(
        name=request.name,
        username=request.username,
        outlet_id=request.outlet_id
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=admin.ShowEmployee)
def update_employee(id: int, request: admin.Employee, db: Session = Depends(database.get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == id)
    if not employee.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Employee with ID {id} is not found')
    employee.update(request.model_dump())
    db.commit()
    return employee.first()


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(id: int, db: Session = Depends(database.get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == id)
    if not employee.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Employee with ID {id} is not found')
    employee.delete(synchronize_session=False)
    db.commit()


@router.get('/employee_by_name/{name}', response_model=admin.ShowEmployee)
def get_employee_by_name(name: str, db: Session = Depends(database.get_db)):
    employee = db.query(models.Employee).filter(models.Employee.name == name)
    if not employee.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Employee with name {name} is not found')
    return employee.first()


@router.get('/employee_by_username/{username}', response_model=admin.ShowEmployee)
def get_employee_by_name(username: str, db: Session = Depends(database.get_db)):
    employee = db.query(models.Employee).filter(models.Employee.username == username)
    if not employee.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Employee with ID {username} is not found')
    return employee.first()


@router.get('/employee_by_outlet/{outlet}', response_model=list[admin.ShowEmployee])
def get_employee_by_outlet(outlet: str, offset: int = 0, limit: int = 10,db: Session = Depends(database.get_db)):
    employee = ((db.query(models.Employee).join(models.Outlet).filter(models.Outlet.name == outlet))
                .offset(offset).limit(limit))

    if not employee.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Employee with outlet name {outlet} is '
                                                                          f'not found')
    return employee.all()
