import smtplib
from email.message import EmailMessage

from .compose import render_template


def send_email(
    smtp_host: str,
    smtp_port: int,
    smtp_user: str | None,
    smtp_pass: str | None,
    sender: str,
    to: str,
    subject: str,
    template: str,
    context: dict,
) -> dict:
    body = render_template(template, context)
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP(host=smtp_host, port=smtp_port, timeout=10) as server:
        if smtp_user and smtp_pass:
            server.starttls()
            server.login(smtp_user, smtp_pass)
        server.send_message(msg)
    return {"ok": True, "to": to}
