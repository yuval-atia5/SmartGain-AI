from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "SmartGain AI is running"}

def test_register_user():
    response = client.post("/users/register", json={
        "name": "Yuval",
        "email": "yuval@test.com",
        "goal": "build_muscle",
        "daily_calories": 3000
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Yuval"
    assert response.json()["email"] == "yuval@test.com"
    assert "id" in response.json()

def test_register_duplicate_email():
    client.post("/users/register", json={
        "name": "Yuval",
        "email": "duplicate@test.com",
        "goal": "build_muscle",
        "daily_calories": 3000
    })
    response = client.post("/users/register", json={
        "name": "Yuval2",
        "email": "duplicate@test.com",
        "goal": "lose_weight",
        "daily_calories": 2000
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_get_user_not_found():
    response = client.get("/users/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"