import random

import database
from data_add_scripts.confdata import client, fake
from models import models

employees_amount = int(input('Enter the number of employees: '))
db = database.SessionLocal()

outlet_ids = [outlet.id for outlet in db.query(models.Outlet).all()]


def add_employees(num=employees_amount):
    for _ in range(num):
        employee_data = {
            'name': fake.name(),
            'username': fake.phone_number(),
            'outlet_id': random.choice(outlet_ids)
        }

        response = client.post(
            '/admin/employee/',
            json=employee_data
        )

        assert response.status_code == 201, response.text

    print(f'Added {num} employees.')


if __name__ == '__main__':
    add_employees()
