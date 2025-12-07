from collections.abc import Generator

import pytest
from flask.testing import FlaskClient

from main import app


@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    app.testing = True
    with app.test_client() as client:
        yield client


@pytest.mark.parametrize(
    "endpoint,lhs,rhs,expected",
    [
        ("/add", 3, 2, 5),
        ("/subtract", 5, 3, 2),
        ("/multiply", 4, 2, 8),
        ("/divide", 10, 2, 5),
    ],
)
def test_operations(
    client: FlaskClient,
    endpoint: str,
    lhs: float,
    rhs: float,
    expected: float
) -> None:
    response = client.get(f"{endpoint}?lhs={lhs}&rhs={rhs}")
    assert response.status_code == 200
    assert response.json is not None
    assert response.json["result"] == expected


def test_divide_by_zero(client: FlaskClient) -> None:
    response = client.get("/divide?lhs=10&rhs=0")
    assert response.status_code == 400
    assert response.json is not None
    assert response.json["error"] == "Cannot divide by zero"


def test_invalid_input(client: FlaskClient) -> None:
    response = client.get("/add?lhs=three&rhs=2")
    assert response.status_code == 400
    assert response.json is not None
    assert response.json["error"] == "Invalid input"
