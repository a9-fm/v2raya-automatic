import requests

from config import config
from src.utils import HEADERS, json_data
from loguru import logger 

def get_subscriptions() -> list[dict]:
    url = f"{config.api_url}/api/subscription"
    headers = HEADERS.copy()

    response = requests.put(url, headers=headers, json=json_data)
    try:
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Ошибка запроса подписок: {e}")
        logger.error(response.text)
        return []

    subs = response.json()
    if subs.get("code") == "SUCCESS" and "data" in subs:
        touch = subs["data"].get("touch", {})
        subscriptions = touch.get("subscriptions", [])
        servers = []
        for i, sub in enumerate(subscriptions):
            for srv in sub.get("servers", []):
                net = str(srv.get("net", "")).lower()
                if any(x in net for x in ["xhttp", "httpupgrade+tls", "httpupgrade"]):
                    continue

                net = srv.get("net", "").lower()
                is_valid = "vless" in net or "ss" in net
                
                if is_valid:
                    # Добавлять sub_index один раз достаточно
                    srv["sub_index"] = i
                    servers.append(srv)
                    logger.debug(f"Добавляем сервер: {srv.get('name')} | Net: {net}")
                else:
                    logger.debug(
                        f"Игнорируем сервер {srv.get('name')} | "
                        f"Net: {net or 'не указан'}, "
                        f"Адрес: {srv.get('address', 'не указан')}"
                    )
        
        count = len(servers)
        logger.info(f"Всего серверов в подписках: {count}")
        return servers
    else:
        logger.error(f"Ошибка получения подписок: {subs.get('message', 'неизвестная ошибка')}")
        return []
