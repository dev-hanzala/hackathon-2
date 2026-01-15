"""
Logging middleware for request/response tracking.
T151: Request/response logging middleware for API debugging and monitoring.
"""

import logging
import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Message

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all incoming requests and outgoing responses."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Log request details and response status with timing.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware/handler in chain

        Returns:
            HTTP response
        """
        # Generate request ID for tracking
        request_id = id(request)

        # Log incoming request
        logger.info(
            f"→ Request [{request_id}]: {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )

        # Log query parameters if present
        if request.url.query:
            logger.debug(f"  Query params [{request_id}]: {request.url.query}")

        # Log request headers (excluding sensitive data)
        headers_to_log = {
            k: v for k, v in request.headers.items() if k.lower() not in ["authorization", "cookie", "set-cookie"]
        }
        logger.debug(f"  Headers [{request_id}]: {headers_to_log}")

        # Start timer
        start_time = time.time()

        try:
            # Process request
            response = await call_next(request)

            # Calculate duration
            duration = time.time() - start_time

            # Log response with color coding based on status
            status_emoji = "✅" if response.status_code < 400 else "⚠️" if response.status_code < 500 else "❌"
            logger.info(
                f"{status_emoji} Response [{request_id}]: {response.status_code} "
                f"for {request.method} {request.url.path} ({duration:.3f}s)"
            )

            # Warn on slow requests (> 1 second)
            if duration > 1.0:
                logger.warning(f"  Slow request [{request_id}]: {duration:.3f}s for {request.url.path}")

            return response

        except Exception as e:
            # Log errors
            duration = time.time() - start_time
            logger.error(
                f"❌ Error [{request_id}]: {type(e).__name__} in {request.method} {request.url.path} "
                f"after {duration:.3f}s - {str(e)}"
            )
            raise


def setup_logging(log_level: str = "INFO") -> None:
    """
    Configure application-wide logging.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Set specific log levels for noisy libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    logger.info(f"✅ Logging configured with level: {log_level}")
