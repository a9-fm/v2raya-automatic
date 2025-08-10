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
    logger.info(f"Пингуем {server['name']}, CODE: {data['code']} | ID: {data['data']['whiches'][0]['id']} | MS: {data['data']['whiches'][0]['pingLatency']}")
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
            results.append((srv, data))
        except Exception as e:
            logger.error(f"Ошибка пинга сервера {srv['name']}: {e}")

    # Записываем good_servers в JSON файл
    try:
        with open("good_servers.json", "w", encoding="utf-8") as f:
            json.dump(good_servers, f, indent=4, ensure_ascii=False)
        logger.info(f"Сохранили {len(good_servers)} валидных серверов в good_servers.json")
    except Exception as e:
        logger.error(f"Ошибка при записи good_servers.json: {e}")

    return results
