from tests.conftest import client


def test_get_order():
    response = client.post(
        '/admin/outlet/',
        json={"name": "Outlet 1 test"}
    )
    assert response.status_code == 201, response.text
    data = response.json()
    outlet_id = data['id']

    response = client.post(
        '/admin/customer',
        json={
            "name": "Cust 1 test",
            "phone": "111111 test",
            "outlet_id": outlet_id
        }
    )
    assert response.status_code == 201, response.text
    data = response.json()
    customer_id = data['id']
    customer_phone = data['phone']

    response = client.post(
        '/admin/employee',
        json={
            "name": "Emp 1 test",
            "username": "111111 test",
            "outlet_id": outlet_id
        }
    )
    assert response.status_code == 201, response.text

    response = client.post(
        f'/order_{customer_phone}',
        json={
            "ended_at": "2023-11-20 20:00:00",
            "where_to_id": outlet_id,
            "performer_id": customer_id
        }
    )
    assert response.status_code == 201, response.text
    data = response.json()
    order_id = data['id']
    order_created_at = data['created_at']
    order_ended_at = data['ended_at']
    order_where_to_id = data['where_to_id']
    order_author_id = data['author_id']
    order_status = data['status']
    order_performer_id = data['performer_id']

    response = client.get(
        f'/order_{customer_phone}'
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert order_id == data[0]['id'], response.text
    assert order_created_at == data[0]['created_at'], response.text
    assert order_ended_at == data[0]['ended_at'], response.text
    assert order_where_to_id == data[0]['where_to_id'], response.text
    assert order_author_id == data[0]['author_id'], response.text
    assert order_status == data[0]['status'], response.text
    assert order_performer_id == data[0]['performer_id'], response.text


def test_update_order():
    response = client.post(
        '/admin/outlet/',
        json={"name": "Outlet 1 test"}
    )
    assert response.status_code == 201, response.text
    data = response.json()
    outlet_id = data['id']

    response = client.post(
        '/admin/customer',
        json={
            "name": "Cust 1 test",
            "phone": "111111 test",
            "outlet_id": outlet_id
        }
    )
    assert response.status_code == 201, response.text
    data = response.json()
    customer_id = data['id']
    customer_phone = data['phone']

    response = client.post(
        '/admin/employee',
        json={
            "name": "Emp 1 test",
            "username": "111111 test",
            "outlet_id": outlet_id
        }
    )
    assert response.status_code == 201, response.text

    response = client.post(
        f'/order_{customer_phone}',
        json={
            "ended_at": "2023-11-20 20:00:00",
            "where_to_id": outlet_id,
            "performer_id": customer_id
        }
    )
    assert response.status_code == 201, response.text
    data = response.json()
    order_id = data['id']

    response = client.put(
        f'order_{customer_phone}_{order_id}',
        json={
            "ended_at": "2023-11-10 10:00:00",
            "where_to_id": outlet_id,
            "performer_id": customer_id
        }
    )
    data = response.json()
    order_id = data['id']
    order_created_at = data['created_at']
    order_ended_at = data['ended_at']
    order_where_to_id = data['where_to_id']
    order_author_id = data['author_id']
    order_status = data['status']
    order_performer_id = data['performer_id']

    response = client.get(
        f'/order_{customer_phone}'
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert order_id == data[0]['id'], response.text
    assert order_created_at == data[0]['created_at'], response.text
    assert order_ended_at == data[0]['ended_at'], response.text
    assert order_where_to_id == data[0]['where_to_id'], response.text
    assert order_author_id == data[0]['author_id'], response.text
    assert order_status == data[0]['status'], response.text
    assert order_performer_id == data[0]['performer_id'], response.text
