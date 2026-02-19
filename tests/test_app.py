import json, pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

def test_home(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"ShopNxt" in res.data

def test_products_shown(client):
    res = client.get("/")
    assert b"Headphones" in res.data
    assert b"Smart Watch" in res.data

def test_health(client):
    res = client.get("/health")
    assert json.loads(res.data)["status"] == "healthy"
