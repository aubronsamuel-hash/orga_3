from __future__ import annotations

import csv
from io import BytesIO, StringIO
from typing import List

from reportlab.lib.pagesizes import A4  # type: ignore[import-not-found, import-untyped, unused-ignore]
from reportlab.pdfgen import canvas  # type: ignore[import-not-found, import-untyped, unused-ignore]


def to_csv_monthly_users(items: List[dict]) -> bytes:
    buf = StringIO()
    w = csv.writer(buf, delimiter=";")
    w.writerow(["user_id", "user_name", "month", "hours_planned", "hours_confirmed", "amount"])
    for it in items:
        w.writerow([
            it["user_id"],
            it["user_name"],
            it["month"],
            f'{it["hours_planned"]:.2f}',
            f'{it["hours_confirmed"]:.2f}',
            f'{it["amount"]:.2f}',
        ])
    return buf.getvalue().encode("utf-8")


def to_pdf_monthly_users(items: List[dict], title: str = "Totaux mensuels par utilisateur") -> bytes:
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4
    y = height - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, title)
    y -= 20
    c.setFont("Helvetica", 9)
    header = ["User", "Mois", "H Prevues", "H Confirmees", "Montant EUR"]
    c.drawString(40, y, " | ".join(header))
    y -= 14
    for it in items:
        line = f'{it["user_name"]} | {it["month"]} | {it["hours_planned"]:.2f} | {it["hours_confirmed"]:.2f} | {it["amount"]:.2f}'
        if y < 40:
            c.showPage()
            y = height - 40
        c.drawString(40, y, line)
        y -= 12
    c.showPage()
    c.save()
    return buf.getvalue()


def to_ics(events: List[dict]) -> bytes:
    # events: [{uid, dtstart, dtend, summary, description}]
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//CoulissesCrew//Reports//FR",
    ]
    for e in events:
        lines += [
            "BEGIN:VEVENT",
            f'UID:{e["uid"]}',
            f'DTSTART:{e["dtstart"].strftime("%Y%m%dT%H%M%SZ")}',
            f'DTEND:{e["dtend"].strftime("%Y%m%dT%H%M%SZ")}',
            f'SUMMARY:{e.get("summary", "Mission")}',
            f'DESCRIPTION:{e.get("description", "")}',
            "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    return ("\r\n".join(lines)).encode("utf-8")
