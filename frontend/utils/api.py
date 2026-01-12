import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

def post(endpoint: str, json=None, headers=None):
    response = requests.post(
        f"{BASE_URL}{endpoint}",
        json=json,
        headers=headers,
        timeout=10
    )
    return response.json()


def get(endpoint: str, headers=None):
    response = requests.get(
        f"{BASE_URL}{endpoint}",
        headers=headers,
        timeout=10
    )
    return response.json()
