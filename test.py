import requests
import uuid
from src.login import get_token
def on_v2raya():
    url = "http://192.168.1.1:2019/api/v2ray"
    
    headers = {
        "Host": "192.168.1.1:2019",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "http://192.168.1.1:2019/",
        "Authorization": get_token(),
        "X-V2raya-Request-Id": str(uuid.uuid4()),
        "Origin": "http://192.168.1.1:2019",
        "Sec-GPC": "1",
        "Connection": "keep-alive",
        "Priority": "u=0",
        "Content-Length": "0"
    }
    
    response = requests.post(url, headers=headers, data=b"")  # пустое тело
    
    try:
        data = response.json()
    except Exception:
        data = response.text
    
    print(f"Status: {response.status_code}")
    print(f"Response: {data}")
    return data

if __name__ == "__main__":
    on_v2raya()
