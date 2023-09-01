from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

import database
from models import models
from schemas import shop

router = APIRouter(
    prefix='/outlets_by_phone',
    tags=['Shop: Get outlets by phone number']
)


@router.get('/outlet_by_phone_number/{phone_number}/', response_model=list[shop.ShowOutlet])
def get_outlet_by_phone_number(phone_number: str, offset: int = 0, limit: int = 10,
                               db: Session = Depends(database.get_db)):
    outlet = (db.query(models.Outlet).join(models.Employee).filter(models.Employee.username == phone_number).
              offset(offset).limit(limit))
    if not outlet.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Access by phone number {phone_number} is forbidden')
    return outlet.all()
