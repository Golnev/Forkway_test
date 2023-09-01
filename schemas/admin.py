from datetime import datetime

from fastapi import Query
from pydantic import BaseModel


class Employee(BaseModel):
    name: str = Query(
        default=...,
        max_length=255,
        description='Employee name',
        examples=['Employee name']
    )
    username: str = Query(
        default=...,
        max_length=255,
        description='Employee phone number',
        examples=['Employee phone number']
    )
    outlet_id: int = Query(
        default=...,
        description='ID of outlet',
        examples=[1]
    )

    class Config:
        orm_mode = True


class ShowEmployee(BaseModel):
    id: int
    name: str
    username: str
    outlet_id: int

    class Config:
        orm_mode = True


class Customer(BaseModel):
    name: str = Query(
        default=...,
        max_length=255,
        description='Customer name',
        examples=['Customer name']
    )
    phone: str = Query(
        default=...,
        max_length=255,
        description='Customer phone number',
        examples=['Customer phone number']
    )
    outlet_id: int = Query(
        default=...,
        description='ID of outlet',
        examples=[1]
    )

    class Config:
        orm_mode = True


class ShowCustomer(BaseModel):
    id: int
    name: str
    phone: str
    outlet_id: int

    class Config:
        orm_mode = True


class Outlet(BaseModel):
    name: str = Query(
        default=...,
        description='Outlet name',
        examples=['Outlet name']
    )

    class Config:
        orm_mode = True


class ShowOutlet(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Order(BaseModel):
    ended_at: datetime = Query(
        default=...,
        description='Date and time of order closing',
        examples=['2023-09-20 20:00:00']
    )
    where_to_id: int = Query(
        default=...,
        description='ID of outlet',
        examples=[1]
    )
    author_id: int = Query(
        default=...,
        description='ID of customer',
        examples=[1]
    )
    status: str = Query(
        default=...,
        description='Order status, must be in (started, ended, in process, awaiting, canceled)',
        examples=['started'],
    )
    performer_id: int = Query(
        default=...,
        description='ID of employee',
        examples=[1]
    )

    class Config:
        orm_mode = True


class ShowOrder(BaseModel):
    id: int
    created_at: datetime
    ended_at: datetime
    where_to_id: int
    author_id: int
    status: str

    class Config:
        orm_mode = True


class OrderStatus(BaseModel):
    status: str = Query(
        default=...,
        description='Order status, must be in (started, ended, in process, awaiting, canceled)',
        examples=['started'],
    )

    class Config:
        orm_mode = True


class Visit(BaseModel):
    performer_id: int = Query(
        default=...,
        description='ID of employee',
        examples=[1]
    )
    order_id: int = Query(
        default=...,
        description='ID of order',
        examples=[1]
    )
    author_id: int = Query(
        default=...,
        description='ID of customer',
        examples=[1]
    )
    where_to_id: int = Query(
        default=...,
        description='ID of outlet',
        examples=[1]
    )

    class Config:
        orm_mode = True


class ShowVisit(BaseModel):
    id: int
    created_at: datetime
    performer_id: datetime
    order_id: int
    author_id: int
    where_to_id: int

    class Config:
        orm_mode = True
