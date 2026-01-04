def test_login_success(client):
    res = client.post("/auth/login", json={"username": "admin", "password": "12345"})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["role"] == "admin"

def test_login_fail(client):
    res = client.post("/auth/login", json={"username": "admin", "password": "wrong"})
    assert res.status_code == 401
