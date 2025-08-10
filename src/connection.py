import requests

from config import config
from src.utils import HEADERS

def connect_server(server_id, sub_index=0, outbound="proxy"):
    url = f"{config.api_url}/api/connection"
    data = {
        "id": server_id,
        "_type": "subscriptionServer",
        "sub": sub_index,
        "outbound": outbound
    }
    resp = requests.post(url, headers=HEADERS, json=data)
    return f"{'SUCCESS' if resp.status_code else {resp.text}}"


def off_v2raya():
    response = requests.delete(f"{config.api_url}/api/v2ray", headers=HEADERS)
    data = response.json()
    if response.status_code == 200:
        data.get("data", {}).get("running")
    else:
        return False

def on_v2raya():
    response = requests.post(f"{config.api_url}/api/v2ray", headers=HEADERS,json={})
    data = response.json()
    if response.status_code == 200:
        data.get("data", {}).get("running")
    else:
        return False