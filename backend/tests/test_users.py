def _login(client):
    res = client.post("/auth/login", json={"username": "admin", "password": "12345"})
    return res.json()["access_token"]

def test_me(client):
    token = _login(client)
    res = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["username"] == "admin"
