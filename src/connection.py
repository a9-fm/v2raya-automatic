import requests

from config import config


import uuid

from src.login import get_token

from urllib.parse import urlparse
import uuid


headers = {
    "Host": "192.168.1.1:2019",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Referer": "http://192.168.1.1:2019/",
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTc1MjUwMzQsInVuYW1lIjoibWlrdSJ9.MWhqbSbQ4CdOrhrpifSYfDWaND0yJ4yjhRpIjNIGj8A",
    "X-V2raya-Request-Id": str(uuid.uuid4()),
    "Origin": "http://192.168.1.1:2019",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Priority": "u=0",
    "Content-Length": "0"
}


import uuid
import requests

from config import config
from src.login import get_token

HEADERS = {
    "Authorization": get_token(),
    "Content-Type": "application/json",
    "X-V2raya-Request-Id": str(uuid.uuid4()),
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Origin": f"{config.api_url}",
    "Referer": f"{config.api_url}",
    "Connection": "keep-alive"
}
def connect_server(server_id, sub_index=0, outbound="proxy"):
    url = f"{config.api_url}/api/connection"
    data = {
        "id": server_id,
        "_type": "subscriptionServer",
        "sub": sub_index,
        "outbound": outbound
    }
    resp = requests.post(url, headers=HEADERS, json=data)
    
    print(data)
    text = f"{'SUCCESS' if resp.status_code else {resp.text}}"
    print(text)
    on_v2raya()
    return text

def off_v2raya():
    response = requests.post(f"{config.api_url}/api/v2ray", headers=headers, data=b"")  # пустое тело
    try:
        data = response.json()
    except Exception:
        data = response.text
    
    print(f"Status: {response.status_code}")
    return data

def on_v2raya():

    
    response = requests.post(f"{config.api_url}/api/v2ray", headers=headers, data=b"")  # пустое тело
    
    try:
        data = response.json()
    except Exception:
        data = response.text
    
    print(f"Status: {response.status_code}")
    return data


