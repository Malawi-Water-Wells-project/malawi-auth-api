from app.main import Application
from json import loads
import re

UUID4_REGEX = re.compile(
    '[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$', re.IGNORECASE)


def test_create_tribe():
    """ Happy path for creating a tribe """

    app = Application("test")
    test_client = app.flask.test_client()

    response = test_client.post("/tribe/create", json={
        "name": "Test Tribe",
        "latitude": 50.5,
        "longitude": 0.1
    })

    assert response.status == "201 CREATED"

    response_body = response.get_json()

    assert response_body.get("status") == "Success"

    created_tribe = response_body.get("tribe", None)

    assert created_tribe is not None
    assert UUID4_REGEX.match(created_tribe.get("public_id"))
    assert created_tribe.get("latitude") == 50.5
    assert created_tribe.get("longitude") == 0.1
    assert created_tribe.get("name") == "Test Tribe"


def test_create_tribe_admin():
    """ Happy path for creating an admin """
    app = Application("test")
    test_client = app.flask.test_client()

    response = test_client.post("/tribe/create", json={
        "name": "Test Tribe",
        "latitude": 50.5,
        "longitude": 0.5
    })

    assert response.status_code == 201

    tribe = response.get_json().get("tribe")

    assert tribe is not None

    tribe_public_id = tribe.get("public_id")
    tribe_private_id = tribe.get("id")
    assert UUID4_REGEX.match(tribe_public_id)

    response = test_client.post(f"/tribe/{tribe_public_id}/admin", json={
        "name": "Test Admin",
        "username": "TestCreateTribeAdminHappyPath",
        "password": "Password"
    })

    assert response.status_code == 201

    admin_created_body = response.get_json()

    assert admin_created_body.get("status") == "Success"

    new_admin = admin_created_body.get("user")

    assert new_admin.get("name") == "Test Admin"
    assert new_admin.get("username") == "TestCreateTribeAdminHappyPath"
    assert new_admin.get("tribe_id") == tribe_private_id
    assert new_admin.get("role") == "tribeadmin"


def test_create_tribe_admin_no_tribe():
    """ Test creating a new tribe admin when the tribe does not exist """

    app = Application("test")
    test_client = app.flask.test_client()

    response = test_client.post("/tribe/nonexistenttribe/admin", json={
        "name": "TestName",
        "username": "Username",
        "password": "Password"
    })

    assert response.status_code == 404
    body = response.get_json()

    assert body.get("status") == "Failure"
    assert body.get("message") == "Tribe not found"


def test_create_tribe_admin_user_taken():
    app = Application("test")
    test_client = app.flask.test_client()

    response = test_client.post("/tribe/create", json={
        "name": "Test Tribe",
        "latitude": 50.5,
        "longitude": 0.5
    })
    assert response.status_code == 201

    tribe_id = response.get_json().get("tribe").get("public_id")

    response = test_client.post(f"/tribe/{tribe_id}/admin", json={
        "name": "TestName",
        "username": "TestDuplicateUser",
        "password": "Password"
    })
    assert response.status_code == 201

    response = test_client.post(f"/tribe/{tribe_id}/admin", json={
        "name": "TestName",
        "username": "TestDuplicateUser",
        "password": "Password"
    })
    assert response.status_code == 400
    body = response.get_json()

    assert body.get("status") == "Failure"
    assert body.get("message") == "Username is already taken"
