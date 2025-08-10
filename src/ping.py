import requests
import urllib.parse
import uuid
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from loguru import logger

from config import config
from src.utils import HEADERS
from src.get_subscriptions import get_subscriptions

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
    logger.info(f"Пингуем {server['name']}, CODE: {data['code']} | ID: {data['data']['whiches'][0]['id']} | MS: {data['data']['whiches'][0]['pingLatency']}")
    return server, data

def ping_all_servers(servers=None) -> list[tuple]:
    if servers is None:
        servers = get_subscriptions()

    results = []
    good_servers = []

    with ThreadPoolExecutor(max_workers=10) as executor:  # Подкорректируй max_workers под себя
        futures = {executor.submit(ping_server, srv): srv for srv in servers}

        for future in as_completed(futures):
            srv = futures[future]
            try:
                srv, data = future.result()
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
                results.append((srv, data))
            except Exception as e:
                logger.error(f"Ошибка пинга сервера {srv['name']}: {e}")

    return results
