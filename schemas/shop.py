from datetime import datetime

from fastapi import Query
from pydantic import BaseModel


class ShowOutlet(BaseModel):
    id: int = Query(
        description='ID of outlet'
    )
    name: str = Query(
        description='Name of outlet'
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
    performer_id: int

    class Config:
        orm_mode = True


class CreateOrder(BaseModel):
    ended_at: datetime = Query(
        default=...,
        description='Date and time of order closing',
        examples=['2023-09-20 20:00:00']
    )
    where_to_id: int
    performer_id: int

    class Config:
        orm_mode = True


class ShowVisit(BaseModel):
    id: int
    created_at: datetime
    performer_id: int
    order_id: int
    author_id: int
    where_to_id: int

    class Config:
        orm_mode = True


class CreateVisit(BaseModel):
    performer_id: int
    order_id: int
    where_to_id: int

    class Config:
        orm_mode = True
