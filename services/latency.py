import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
# Set up logging
logger = logging.getLogger("latency_logger")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("latency.log")
formatter = logging.Formatter("%(asctime)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
class RouteLatencyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start_time
        route = request.scope.get("route")
        route_path = route.path if route else request.url.path
        logger.info(f"{request.method} {route_path} took {duration:.4f}s")
        response.headers["X-Process-Time"] = f"{duration:.4f}"
        return response
