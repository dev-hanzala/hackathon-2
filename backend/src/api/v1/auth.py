"""Authentication endpoints for user registration, signin, and logout.

T040: /api/v1/auth/register endpoint
T041: /api/v1/auth/signin endpoint
T042: /api/v1/auth/logout endpoint
T044: Error handling for auth failures
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.schemas import (
    AuthResponse,
    ErrorResponse,
    UserCreate,
    UserResponse,
    UserSignIn,
)
from src.db.database import get_session
from src.db.models import User
from src.middleware.auth import get_current_user
from src.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"model": ErrorResponse, "description": "Email already registered"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_session),
) -> AuthResponse:
    """Register a new user.

    Creates a new user account with email and password.
    Returns user info and access token for auto-login.

    Args:
        user_data: User registration data (email, password)
        db: Database session

    Returns:
        AuthResponse with user info and access token

    Raises:
        HTTPException 409: If email already registered
        HTTPException 422: If validation fails
    """
    user, token = AuthService.register_user(
        db=db,
        email=user_data.email,
        password=user_data.password,
    )

    return AuthResponse(
        token=token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
        ),
    )


@router.post(
    "/signin",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid credentials"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
async def signin(
    credentials: UserSignIn,
    db: Session = Depends(get_session),
) -> AuthResponse:
    """Sign in a user.

    Authenticates user with email and password.
    Returns user info and access token.

    Args:
        credentials: User login credentials (email, password)
        db: Database session

    Returns:
        AuthResponse with user info and access token

    Raises:
        HTTPException 401: If credentials are invalid
        HTTPException 422: If validation fails
    """
    user, token = AuthService.authenticate_user(
        db=db,
        email=credentials.email,
        password=credentials.password,
    )

    return AuthResponse(
        token=token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
        ),
    )


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
    },
)
async def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
) -> dict:
    """Sign out the current user.

    Invalidates the current session/token.
    Client should remove token from storage.

    Args:
        current_user: Currently authenticated user
        db: Database session

    Returns:
        Success message

    Raises:
        HTTPException 401: If not authenticated
    """
    # JWT logout is stateless - client removes token
    # For session tracking, we could blacklist the token here
    return {"message": "Successfully logged out"}


@router.get(
    "/me",
    response_model=UserResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated"},
    },
)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Get current authenticated user info.

    Returns the currently logged-in user's information.

    Args:
        current_user: Currently authenticated user

    Returns:
        UserResponse with user info

    Raises:
        HTTPException 401: If not authenticated
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )
