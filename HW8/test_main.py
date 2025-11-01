from fastapi.testclient import TestClient

from main import app

# init test client
client = TestClient(app)


# GET testing
def test_get_summ():
    # '%2b' => '+' (in URL-code)
    response = client.get("/calc?expression=32%2b3")
    assert response.status_code == 200
    assert response.json()['result'] == '35'


def test_get_diff():
    response = client.get("/calc?expression=1-2")
    assert response.status_code == 200
    assert response.json()['result'] == '-1'


def test_get_mult():
    response = client.get("/calc?expression=2*2")
    assert response.status_code == 200
    assert response.json()['result'] == '4'


def test_get_dev():
    response = client.get("/calc?expression=5/2")
    assert response.status_code == 200
    assert response.json()['result'] == '2.5'


# POST testing
def test_post_summ():
    response = client.post(
        "/calc", json={'operator': '+', 'first': '10', 'last': '5'})
    assert response.status_code == 200
    assert response.json()['result'] == '15'


def test_post_diff():
    response = client.post(
        "/calc", json={'operator': '-', 'first': '5', 'last': '3'})
    assert response.status_code == 200
    assert response.json()['result'] == '2'


def test_post_mult():
    response = client.post(
        "/calc", json={'operator': '*', 'first': '2', 'last': '2'})
    assert response.status_code == 200
    assert response.json()['result'] == '4'


def test_post_dev():
    response = client.post(
        "/calc", json={'operator': '/', 'first': '11', 'last': '2'})
    assert response.status_code == 200
    assert response.json()['result'] == '5.5'
