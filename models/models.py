from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, CheckConstraint, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    username = Column(String(length=255))
    outlet_id = Column(Integer, ForeignKey('outlets.id'), nullable=False)
    outlet = relationship("Outlet")


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    phone = Column(String(length=255))
    outlet_id = Column(Integer, ForeignKey('outlets.id'), nullable=False)
    outlet = relationship("Outlet")


class Outlet(Base):
    __tablename__ = 'outlets'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    employees = relationship("Employee", back_populates="outlet")


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    ended_at = Column(TIMESTAMP(timezone=True))
    where_to_id = Column(Integer, ForeignKey('outlets.id'))
    author_id = Column(Integer, ForeignKey('customers.id'))
    status = Column(String,
                    CheckConstraint("status IN ('started', 'ended', 'in process', 'awaiting', 'canceled')"))
    performer_id = Column(Integer, ForeignKey('employees.id'))


class Visit(Base):
    __tablename__ = 'visits'

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True), default=func.now())
    performer_id = Column(Integer, ForeignKey('employees.id'))
    order_id = Column(Integer, ForeignKey('orders.id'), unique=True)
    author_id = Column(Integer, ForeignKey('customers.id'))
    where_to_id = Column(Integer, ForeignKey('outlets.id'))
