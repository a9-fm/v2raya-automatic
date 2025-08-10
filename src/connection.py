import requests
import urllib.parse
import uuid
import json
from config import config
from src.utils import HEADERS
from src.get_subscriptions import get_subscriptions

from loguru import logger

def ping_server(server) -> dict:
    whiches = [{
        "id": server["id"],
        "_type": server["_type"],
        "sub": server.get("sub_index", 0)
    }]
    param = urllib.parse.quote(json.dumps(whiches))
    url = f"{config.api_url}/api/httpLatency?whiches={param}"

    headers = HEADERS.copy()
    headers["X-V2raya-Request-Id"] = str(uuid.uuid4())

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    logger.info(f"Пингуем {server['name']}, ответ: {json.dumps(data, indent=2, ensure_ascii=False)}")
    return data

def ping_all_servers(servers=None) -> dict:
    results = []
    good_servers = []

    if not servers:
        servers = get_subscriptions()

    for srv in servers:
        try:
            data = ping_server(srv)

            if data.get("code") == "SUCCESS":
                which = data["data"]["whiches"][0]
                latency_str = which.get("pingLatency", "").replace("ms", "").strip()

                if latency_str.isdigit():
                    latency = int(latency_str)
                    if latency < 400:
                        good_servers.append({
                            "name": srv["name"],
                            "id": srv["id"],
                            "latency_ms": latency
                        })
                        logger.info(f"{srv['name']} | {srv['id']} | {latency}ms")

            results.append((srv, data))
        except Exception as e:
            logger.error(f"Ошибка пинга сервера {srv['name']}: {e}")

    return results
