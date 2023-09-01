from datetime import datetime, timezone

from sqlalchemy import func

import database
from data_add_scripts.confdata import client
from models import models

visits_amount = int(input('Enter the number of orders: '))
db = database.SessionLocal()

today = datetime.now(timezone.utc)


def add_visits(num=visits_amount):
    visits_count = 0
    while visits_count != num:
        customer = db.query(models.Customer).order_by(func.random()).first()

        order = (db.query(models.Order).join(models.Customer)
                 .filter(customer.id == models.Order.author_id)
                 .filter(models.Order.ended_at > today)
                 .order_by(func.random())
                 .first())

        if not order:
            continue

        visits_in_db = db.query(models.Visit).filter(models.Visit.order_id == order.id).first()
        if visits_in_db:
            continue

        visit_data = {
            "performer_id": order.performer_id,
            "order_id": order.id,
            "where_to_id": order.where_to_id
        }

        response = client.post(
            f'/visit_{customer.phone}/',
            json=visit_data
        )

        assert response.status_code == 201, response.text

        visits_count += 1

    print(f'Added {visits_count} customers.')


if __name__ == '__main__':
    add_visits()
