from tests.conftest import client


def test_add_outlet():
    response = client.post(
        '/admin/outlet/',
        json={"name": "Outlet 1 test"}
    )
    assert response.status_code == 201, response.text

    data = response.json()

    outlet_name = data['name']
    outlet_id = data['id']

    response = client.get(
        f'/admin/outlet/outlet_by_name/{outlet_name}/'
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['name'] == 'Outlet 1 test'
    assert data['id'] == outlet_id


def test_put_outlet():
    response = client.post(
        '/admin/outlet/',
        json={"name": "Outlet 1 test"}
    )
    assert response.status_code == 201, response.text

    data = response.json()
    outlet_id = data['id']

    response = client.put(
        f'/admin/outlet/{outlet_id}',
        json={"name": "Outlet 2 test"}
    )
    assert response.status_code == 202, response.text

    data = response.json()

    outlet_name = data['name']
    outlet_id = data['id']

    response = client.get(
        f'/admin/outlet/outlet_by_name/{outlet_name}/'
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['name'] == outlet_name
    assert data['id'] == outlet_id


def test_get_outlet_by_employee():
    response = client.post(
        '/admin/outlet/',
        json={"name": "Outlet 1 test"}
    )
    assert response.status_code == 201, response.text
    data = response.json()
    outlet_name = data['name']
    outlet_id = data['id']

    response = client.post(
        '/admin/employee/',
        json={
            "name": "Emp 1 Test",
            "username": "111111 test",
            "outlet_id": outlet_id
        }
    )
    assert response.status_code == 201, response.text
    data = response.json()
    employee_username = data['username']

    response = client.get(
        f'/admin/outlet/outlet_by_employee/{employee_username}'
    )
    data = response.json()
    assert response.status_code == 200, response.text
    assert data[0]['id'] == outlet_id, response.text
    assert data[0]['name'] == outlet_name, response.text
