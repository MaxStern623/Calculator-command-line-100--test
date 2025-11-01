import subprocess
import time
import requests


BASE = 'http://127.0.0.1:8000'


def test_api_end_to_end():
    # assume the server is already running locally; check /history and /calc
    r = requests.get(f'{BASE}/history')
    assert r.status_code == 200

    r = requests.get(f'{BASE}/calc?expression=3%2b4')
    assert r.status_code == 200
    assert r.json()['result'] == '7'
