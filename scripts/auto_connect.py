from src.ping import ping_all_servers
from src.get_subscriptions import get_subscriptions
from loguru import logger

from src.connection import connect_server, on_v2raya

def get_fastest_server():
    servers = get_subscriptions()  # Получаем список серверов
    good_servers = []

    for srv in servers:
        try:
            data = ping_all_servers([srv])
            if not data:
                continue
            _, resp = data[0]
            if resp.get("code") == "SUCCESS":
                which = resp["data"]["whiches"][0]
                latency_str = which.get("pingLatency", "").replace("ms", "").strip()
                if latency_str.isdigit():
                    latency = int(latency_str)
                    if latency < 400:
                        good_servers.append({
                            "id": srv["id"],
                            "latency_ms": latency
                        })
        except Exception as e:
            logger.error(f"Ошибка при пинге сервера {srv['name']}: {e}")

    if not good_servers:
        return None

    # Находим сервер с минимальным latency
    fastest = min(good_servers, key=lambda x: x["latency_ms"])
    return fastest

if __name__ == "__main__":
    fastest = get_fastest_server()
    if fastest:
        logger.info(f"ID самого быстрого сервера: {fastest['id']}, задержка: {fastest['latency_ms']}ms")
        try:
            on_v2raya()
            connect_server(fastest['id'])
            logger.success("Подключили вас к серверу")
        except Exception as e:
            logger.error(f"Ошибка при подключении к серверу {fastest['id']}: {e}")
    else:
        logger.warning("Нет подходящих серверов с latency < 400ms")
