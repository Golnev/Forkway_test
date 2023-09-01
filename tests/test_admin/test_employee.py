from tests.conftest import client


def get_employee(employee_id, employee_name, employee_username, employee_outlet_id, outlet_name):
    response = client.get(
        f'/admin/employee/employee_by_name/{employee_name}'
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['id'] == employee_id, response.text
    assert data['name'] == employee_name, response.text
    assert data['username'] == employee_username, response.text
    assert data['outlet_id'] == employee_outlet_id, response.text

    response = client.get(
        f'/admin/employee/employee_by_username/{employee_username}'
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['id'] == employee_id, response.text
    assert data['name'] == employee_name, response.text
    assert data['username'] == employee_username, response.text
    assert data['outlet_id'] == employee_outlet_id, response.text

    response = client.get(
        f'/admin/employee/employee_by_outlet/{outlet_name}'
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]['id'] == employee_id, response.text
    assert data[0]['name'] == employee_name, response.text
    assert data[0]['username'] == employee_username, response.text
    assert data[0]['outlet_id'] == employee_outlet_id, response.text


def test_add_employee():
    response = client.post(
        '/admin/outlet/',
        json={"name": "Outlet 1 test"}
    )
    assert response.status_code == 201, response.text
    data = response.json()
    outlet_name = data['name']
    outlet_id = data['id']

    response = client.post(
        '/admin/employee',
        json={
            "name": "Emp 1 test",
            "username": "111111 test",
            "outlet_id": outlet_id
        }
    )
    assert response.status_code == 201, response.text
    data = response.json()
    employee_id = data['id']
    employee_name = data['name']
    employee_username = data['username']
    employee_outlet_id = data['outlet_id']

    get_employee(employee_id, employee_name, employee_username, employee_outlet_id, outlet_name)


def test_update_employee():
    response = client.post(
        '/admin/outlet/',
        json={"name": "Outlet 1 test"}
    )
    assert response.status_code == 201, response.text
    data = response.json()
    outlet_name = data['name']
    outlet_id = data['id']

    response = client.post(
        '/admin/employee',
        json={
            "name": "Emp 1 test",
            "username": "111111 test",
            "outlet_id": outlet_id
        }
    )
    assert response.status_code == 201, response.text
    data = response.json()
    employee_id = data['id']

    response = client.put(
        f'/admin/employee/{employee_id}',
        json={
            "name": "Update Emp 1 Test",
            "username": "Update 111111 test",
            "outlet_id": outlet_id
        }
    )
    assert response.status_code == 202, response.text
    data = response.json()
    employee_id = data['id']
    employee_name = data['name']
    employee_username = data['username']
    employee_outlet_id = data['outlet_id']

    get_employee(employee_id, employee_name, employee_username, employee_outlet_id, outlet_name)
