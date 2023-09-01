import random

import database
from data_add_scripts.confdata import fake, client
from models import models

customers_amount = int(input('Enter the number of customers: '))
db = database.SessionLocal()

outlet_ids = [outlet.id for outlet in db.query(models.Outlet).all()]


def add_customers(num=customers_amount):
    for _ in range(num):
        customer_data = {
            "name": fake.company(),
            "phone": fake.phone_number(),
            "outlet_id": random.choice(outlet_ids)
        }

        response = client.post(
            '/admin/customer/',
            json=customer_data
        )

        assert response.status_code == 201, response.text

    print(f'Added {num} customers.')


if __name__ == '__main__':
    add_customers()
