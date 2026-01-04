def _login(client):
    res = client.post("/auth/login", json={"username": "admin", "password": "12345"})
    return res.json()["access_token"]

def test_reports_requires_auth(client):
    res = client.get("/reports/works")
    assert res.status_code in (401, 403)
