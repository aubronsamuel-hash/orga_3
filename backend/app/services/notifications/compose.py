from pathlib import Path

TEMPLATES = {
    "invite": "invite.txt",
    "reminder": "reminder.txt",
    "schedule_change": "schedule_change.txt",
    "cancellation": "cancellation.txt",
}


def load_template(name: str) -> str:
    fp = (
        Path(__file__).resolve().parents[2]
        / "templates"
        / "notifications"
        / TEMPLATES[name]
    )
    return fp.read_text(encoding="utf-8")


def render_template(name: str, context: dict) -> str:
    content = load_template(name)
    for k, v in context.items():
        content = content.replace("{{" + k + "}}", str(v))
    return content
