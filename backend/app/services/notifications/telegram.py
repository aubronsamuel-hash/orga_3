import json
import urllib.request


def send_telegram(bot_token: str, chat_id: str, text: str) -> dict:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = json.dumps({"chat_id": chat_id, "text": text}).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
        return {
            "ok": bool(payload.get("ok")),
            "message_id": payload.get("result", {}).get("message_id"),
        }
