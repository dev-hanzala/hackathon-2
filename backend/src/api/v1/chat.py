"""Chat API endpoints using Gemini via the OpenAI SDK."""

import logging

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.schemas import ChatRequest, ChatResponse
from src.config import settings
from src.db.models import User
from src.middleware.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post(
    "",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Send a chat message to Gemini",
    responses={
        500: {"description": "Gemini API error"},
        503: {"description": "Gemini API key not configured"},
    },
)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Send messages to the Gemini model and get a response.

    Requires authentication. Uses the OpenAI SDK to communicate
    with Google's Gemini API via its OpenAI-compatible endpoint.
    """
    if not settings.gemini_api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Chat service is not configured. Set GEMINI_API_KEY.",
        )

    from src.services.chat_service import ChatService

    logger.info(f"Chat request from user {current_user.id}: {len(request.messages)} messages")

    try:
        messages = [{"role": m.role, "content": m.content} for m in request.messages]
        response_text = ChatService.chat(
            messages=messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat service error: {e}",
        ) from e

    return ChatResponse(
        response=response_text,
        model=request.model or settings.gemini_model,
    )
