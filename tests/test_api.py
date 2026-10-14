from fastapi.testclient import TestClient

from repairbot.api.experiment.api import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_hello():
    response = client.get("/hello/test")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello, test!"}


def test_post_user():
    response = client.post("/users", json={"name": "Marci", "age": 99})

    assert response.status_code == 201
    assert response.json() == {
        "message": "User created",
        "user": {"name": "Marci", "age": 99},
    }


def test_post_user_invalid_age():
    response = client.post("/users", json={"name": "Marci", "age": 150})

    assert response.status_code == 422
