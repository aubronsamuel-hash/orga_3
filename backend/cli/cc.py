from __future__ import annotations

import os
import sys
import requests
import typer

app = typer.Typer(help="CLI cc")
API_BASE = os.environ.get("API_BASE", "http://localhost:8000")


@app.command("version")
def version() -> None:
    typer.echo("cc 0.1.0")


@app.command("env")
def env() -> None:
    typer.echo(f"API_BASE={API_BASE}")


@app.command("ping")
def ping() -> None:
    try:
        r = requests.get(f"{API_BASE}/health")
        typer.echo(f"PING OK {r.status_code}")
        raise SystemExit(0)
    except Exception:
        typer.echo("ERREUR reseau API", err=True)
        raise SystemExit(4)


@app.command("reports")
def reports_monthly_users(
    org_id: str = typer.Option(..., "--org-id"),
    project_id: str = typer.Option(None, "--project-id"),
    date_from: str = typer.Option(..., "--date-from"),
    date_to: str = typer.Option(..., "--date-to"),
) -> None:
    url = f"{API_BASE}/api/v1/reports/monthly-users"
    try:
        r = requests.get(
            url,
            params=dict(
                org_id=org_id,
                project_id=project_id,
                date_from=date_from,
                date_to=date_to,
            ),
            timeout=30,
        )
        r.raise_for_status()
        typer.echo(r.text)
        raise SystemExit(0)
    except requests.exceptions.HTTPError as e:
        typer.echo(
            f"ERREUR HTTP: {e.response.status_code} {e.response.text}", err=True
        )
        raise SystemExit(4)
    except requests.exceptions.Timeout:
        typer.echo("TIMEOUT", err=True)
        raise SystemExit(3)
    except requests.exceptions.RequestException as e:  # pragma: no cover - network
        typer.echo(f"ERREUR reseau: {e}", err=True)
        raise SystemExit(4)


if __name__ == "__main__":
    app()
