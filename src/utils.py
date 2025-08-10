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

json_data = {
    "id": 1,
    "_type": "subscription"
}


