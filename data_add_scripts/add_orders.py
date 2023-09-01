import random
from datetime import datetime, timezone, timedelta

from sqlalchemy import func

import database
from data_add_scripts.confdata import client
from models import models

orders_amount = int(input('Enter the number of orders: '))
db = database.SessionLocal()

today = datetime.now(timezone.utc)
six_months_from_now = today + timedelta(days=180)


def add_orders(num=orders_amount):
    orders_count = 0
    while orders_count != num:
        customer = db.query(models.Customer).order_by(func.random()).first()

        employee = (db.query(models.Employee).join(models.Outlet)
                    .filter(models.Employee.outlet_id == customer.outlet_id).order_by(func.random()).first())

        if not employee:
            continue

        ended_at = today + timedelta(days=random.randint(1, (six_months_from_now - today).days))

        order_data = {
            "ended_at": str(ended_at),
            "where_to_id": customer.outlet_id,
            "performer_id": employee.id
        }

        response = client.post(
            f'/order_{customer.phone}/',
            json=order_data
        )
        assert response.status_code == 201, response.text

        orders_count += 1

    print(f'Added {orders_count} customers.')


if __name__ == '__main__':
    add_orders()
