import os
import requests

API_URL = "https://ursh-enterprise.onrender.com"

class APIError(Exception):
    pass

def _headers(token: str | None):
    h = {"Accept": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h

def login(username: str, password: str):
    r = requests.post(f"{API_URL}/auth/login", json={"username": username, "password": password}, timeout=20)
    if r.status_code != 200:
        return None
    return r.json()

def register(payload: dict):
    r = requests.post(f"{API_URL}/auth/register", json=payload, timeout=20)
    if r.status_code != 200:
        raise APIError(r.json().get("detail", "Registration failed"))
    return r.json()

def me(token: str):
    r = requests.get(f"{API_URL}/users/me", headers=_headers(token), timeout=20)
    if r.status_code != 200:
        raise APIError("Unauthorized")
    return r.json()

def departments(token: str | None = None):
    r = requests.get(f"{API_URL}/org/departments", headers=_headers(token), timeout=20)
    r.raise_for_status()
    return r.json()

def teams(token: str | None = None, department_id: int | None = None):
    params = {}
    if department_id is not None:
        params["department_id"] = department_id
    r = requests.get(f"{API_URL}/org/teams", params=params, headers=_headers(token), timeout=20)
    r.raise_for_status()
    return r.json()

def department_full(token: str, dept_id: int):
    r = requests.get(f"{API_URL}/org/departments/{dept_id}/full", headers=_headers(token), timeout=20)
    r.raise_for_status()
    return r.json()

def reports_works(token: str, params: dict):
    r = requests.get(f"{API_URL}/reports/works", params=params, headers=_headers(token), timeout=30)
    r.raise_for_status()
    return r.json()

def export_excel(token: str, params: dict):
    r = requests.get(f"{API_URL}/exports/works/excel", params=params, headers=_headers(token), timeout=60)
    r.raise_for_status()
    return r.content, r.headers.get("Content-Disposition", "attachment; filename=report.xlsx")

def create_work(token: str, payload: dict):
    r = requests.post(f"{API_URL}/works", json=payload, headers=_headers(token), timeout=30)
    if r.status_code != 200:
        raise APIError(r.json().get("detail", "Create failed"))
    return r.json()

def update_work(token: str, work_id: int, payload: dict):
    r = requests.put(f"{API_URL}/works/{work_id}", json=payload, headers=_headers(token), timeout=30)
    if r.status_code != 200:
        raise APIError(r.json().get("detail", "Update failed"))
    return r.json()

def delete_work(token: str, work_id: int):
    r = requests.delete(f"{API_URL}/works/{work_id}", headers=_headers(token), timeout=30)
    if r.status_code != 200:
        raise APIError(r.json().get("detail", "Delete failed"))
    return r.json()

def change_password(token: str, new_password: str):
    r = requests.post(f"{API_URL}/users/change-password", json={"new_password": new_password}, headers=_headers(token), timeout=30)
    if r.status_code != 200:
        raise APIError(r.json().get("detail", "Password change failed"))
    return r.json()

def add_user_manual(token: str, payload: dict):
    r = requests.post(f"{API_URL}/users/manual", json=payload, headers=_headers(token), timeout=30)
    if r.status_code != 200:
        raise APIError(r.json().get("detail", "Add user failed"))
    return r.json()

def export_cv(token: str, user_id: int):
    r = requests.get(f"{API_URL}/exports/users/{user_id}/cv.pdf", headers=_headers(token), timeout=60)
    if r.status_code != 200:
        raise APIError(r.json().get("detail", "CV export failed"))
    return r.content, r.headers.get("Content-Disposition", "attachment; filename=CV.pdf")
