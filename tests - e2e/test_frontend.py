import requests


def test_frontend_available():
    response = requests.get("http://localhost:3000/")
    assert response.status_code == 200
