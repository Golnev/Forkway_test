from data_add_scripts.confdata import fake, client

outlets_amount = int(input('Enter the number of outlets: '))


def add_outlets(num=outlets_amount):
    for _ in range(num):
        outlet_data = {
            'name': fake.large_company()
        }

        response = client.post('/admin/outlet/', json=outlet_data)

        assert response.status_code == 201, response.text

    print(f'Added {num} outlets.')


if __name__ == '__main__':
    add_outlets()
