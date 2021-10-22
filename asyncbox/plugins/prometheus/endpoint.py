"""Prometheus endpoint for bot's metrics."""
import os

from fastapi import APIRouter
from prometheus_client.exposition import CONTENT_TYPE_LATEST  # type: ignore
from prometheus_client.exposition import generate_latest
from prometheus_client.multiprocess import MultiProcessCollector  # type: ignore
from prometheus_client.registry import REGISTRY  # type: ignore
from prometheus_client.registry import CollectorRegistry
from starlette.responses import Response

router = APIRouter()


@router.get("/metrics", name="prometheus:metrics")
async def metrics() -> Response:
    """Endpoint to get all bot's metrics."""
    if "prometheus_multiproc_dir" in os.environ:  # pragma: no cover
        registry = CollectorRegistry()
        MultiProcessCollector(registry)
    else:
        registry = REGISTRY

    return Response(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)
