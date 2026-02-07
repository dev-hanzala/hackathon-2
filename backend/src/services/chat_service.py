"""Chat service using OpenAI SDK to access Google Gemini API."""

import logging

from openai import OpenAI

from src.config import settings

logger = logging.getLogger(__name__)

# Gemini's OpenAI-compatible endpoint
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"


def get_gemini_client() -> OpenAI:
    """Create an OpenAI client configured for Gemini."""
    if not settings.gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not configured")

    return OpenAI(
        api_key=settings.gemini_api_key,
        base_url=GEMINI_BASE_URL,
    )


class ChatService:
    """Service for chat completions via Gemini using the OpenAI SDK."""

    @staticmethod
    def chat(
        messages: list[dict[str, str]],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> str:
        """
        Send a chat completion request to Gemini via the OpenAI SDK.

        Args:
            messages: List of message dicts with 'role' and 'content' keys.
            model: Model name override (defaults to settings.gemini_model).
            temperature: Sampling temperature (0.0 - 2.0).
            max_tokens: Maximum tokens in the response.

        Returns:
            The assistant's response text.
        """
        client = get_gemini_client()
        model = model or settings.gemini_model

        logger.info(f"Sending chat request to Gemini model={model}, messages={len(messages)}")

        kwargs: dict = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        if max_tokens is not None:
            kwargs["max_tokens"] = max_tokens

        response = client.chat.completions.create(**kwargs)

        content = response.choices[0].message.content or ""
        logger.info(f"Gemini response received: {len(content)} chars")
        return content
