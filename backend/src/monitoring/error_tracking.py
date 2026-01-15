"""
Error tracking and monitoring configuration.
T152: Sentry integration for production error visibility.
"""

import logging
from typing import Literal

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

logger = logging.getLogger(__name__)


def setup_error_tracking(
    dsn: str | None,
    environment: str = "development",
    traces_sample_rate: float = 1.0,
    profiles_sample_rate: float = 1.0,
    debug: bool = False,
) -> None:
    """
    Initialize Sentry error tracking and performance monitoring.

    Args:
        dsn: Sentry Data Source Name (DSN) URL
        environment: Environment name (development, staging, production)
        traces_sample_rate: Percentage of transactions to trace (0.0 to 1.0)
        profiles_sample_rate: Percentage of transactions to profile (0.0 to 1.0)
        debug: Enable Sentry debug mode
    """
    if not dsn:
        logger.info("⚠️ Sentry DSN not configured - error tracking disabled")
        return

    try:
        sentry_sdk.init(
            dsn=dsn,
            environment=environment,
            # Performance monitoring
            traces_sample_rate=traces_sample_rate,
            profiles_sample_rate=profiles_sample_rate,
            # Integrations
            integrations=[
                FastApiIntegration(
                    transaction_style="url",  # Group by URL pattern, not specific IDs
                    failed_request_status_codes=[403, range(500, 599)],  # Report 403 and 5xx errors
                ),
                SqlalchemyIntegration(),
            ],
            # Additional options
            debug=debug,
            send_default_pii=False,  # Don't send personally identifiable information
            attach_stacktrace=True,  # Include stack traces for all messages
            # Release tracking (optional, can be set from environment)
            # release="todo-api@0.1.0",
        )

        logger.info(f"✅ Sentry error tracking initialized for environment: {environment}")

    except Exception as e:
        logger.error(f"❌ Failed to initialize Sentry: {e}")
        # Don't fail application startup if Sentry fails
        pass


def capture_exception(error: Exception, context: dict | None = None) -> None:
    """
    Manually capture an exception to Sentry with optional context.

    Args:
        error: Exception to capture
        context: Additional context dict to include with error
    """
    try:
        if context:
            with sentry_sdk.push_scope() as scope:
                for key, value in context.items():
                    scope.set_context(key, value)
                sentry_sdk.capture_exception(error)
        else:
            sentry_sdk.capture_exception(error)
    except Exception as e:
        logger.error(f"Failed to capture exception in Sentry: {e}")


def capture_message(
    message: str,
    level: Literal["fatal", "critical", "error", "warning", "info", "debug"] = "info",
    context: dict | None = None,
) -> None:
    """
    Capture a message to Sentry with optional context.

    Args:
        message: Message to capture
        level: Severity level (debug, info, warning, error, fatal)
        context: Additional context dict to include with message
    """
    try:
        if context:
            with sentry_sdk.push_scope() as scope:
                for key, value in context.items():
                    scope.set_context(key, value)
                sentry_sdk.capture_message(message, level=level)
        else:
            sentry_sdk.capture_message(message, level=level)
    except Exception as e:
        logger.error(f"Failed to capture message in Sentry: {e}")
