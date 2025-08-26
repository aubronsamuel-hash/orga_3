from __future__ import annotations

import time
from typing import Callable, Awaitable

from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    CONTENT_TYPE_LATEST,
    generate_latest,
)
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, PlainTextResponse
from starlette.routing import Match

# Metrics (noms stables)

REQUESTS = Counter(
    "app_requests_total",
    "Total des requetes HTTP",
    ["method", "path", "status"],
)
DURATION = Histogram(
    "app_request_duration_seconds",
    "Duree des requetes HTTP (secondes)",
    ["method", "path", "status"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)
INFLIGHT = Gauge(
    "app_inflight_requests",
    "Requetes HTTP en cours",
)

def _path_template(request: Request) -> str:
    # Essaie de trouver le pattern de route (ex: /api/v1/projects)
    for route in request.app.router.routes:
        match, _ = route.matches(request.scope)
        if match == Match.FULL:
            try:
                return route.path
            except Exception:
                continue
    return request.url.path


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        path = _path_template(request)
        method = request.method.upper()
        start = time.perf_counter()
        INFLIGHT.inc()
        try:
            response = await call_next(request)
            status = str(response.status_code)
            elapsed = time.perf_counter() - start
            REQUESTS.labels(method=method, path=path, status=status).inc()
            DURATION.labels(method=method, path=path, status=status).observe(elapsed)
            return response
        finally:
            INFLIGHT.dec()


async def metrics_endpoint(_: Request) -> Response:
    output = generate_latest()  # default registry
    return PlainTextResponse(output.decode("utf-8"), media_type=CONTENT_TYPE_LATEST)


def setup_metrics(app, enabled: bool = True) -> None:
    if not enabled:
        return
    app.add_route("/metrics", metrics_endpoint, methods=["GET"])
    app.add_middleware(MetricsMiddleware)
