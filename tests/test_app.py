import pytest
from src.app import app, load_database, save_database
import json
import os

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def test_db():
    test_data = {
        "users": [
            {"id": 1, "name": "Test User", "email": "test@example.com"}
        ],
        "posts": [
            {"id": 1, "title": "Test Post", "content": "This is a test post"}
        ]
    }
    save_database(test_data)
    yield test_data
    if os.path.exists("data/db.json"):
        os.remove("data/db.json")

def test_get_users(client, test_db):
    response = client.get('/api/users')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]["name"] == "Test User"

def test_create_user(client):
    user_data = {
        "name": "New User",
        "email": "new@example.com"
    }
    response = client.post('/api/users', json=user_data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["message"] == "User created successfully"

def test_get_posts(client, test_db):
    response = client.get('/api/posts')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]["title"] == "Test Post"

def test_create_post(client):
    post_data = {
        "title": "New Post",
        "content": "This is a new post"
    }
    response = client.post('/api/posts', json=post_data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["message"] == "Post created successfully" 