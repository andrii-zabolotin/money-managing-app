import pytest

from tests.conftest import client
from starlette.testclient import TestClient


def test_user_register_success(client: TestClient):
    """Tests that user registration is successful."""

    response = client.post("/auth/register", json={
        "email": "test333@gmail.com",
        "password": "testpassword",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string"
    })

    assert response.status_code == 201, "Client wasn't created!"


@pytest.mark.dependency(depends=["test_user_register_success"])
def test_user_exists_error(client: TestClient):
    """Tests that if user already exists error return"""

    response = client.post("/auth/register", json={
        "email": "test333@gmail.com",
        "password": "testpassword",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string"
    })

    assert response.status_code == 400
    assert response.json() == {'detail': 'REGISTER_USER_ALREADY_EXISTS'}


@pytest.mark.dependency(depends=["test_user_register_success"])
def test_short_password_error(client: TestClient):
    """Tests that short password validation error return"""

    response = client.post("/auth/register", json={
        "email": "test334@gmail.com",
        "password": "t",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string"
    })

    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == 'String should have at least 5 characters'


@pytest.mark.dependency(depends=["test_user_register_success"])
def test_jwt_token_success(client: TestClient):
    """Tests that the JWT login is successful."""

    response = client.post("/auth/jwt/login", data={
        "username": "test333@gmail.com",
        "password": "testpassword"
    })

    assert response.status_code == 204, "Unsuccessful login"
