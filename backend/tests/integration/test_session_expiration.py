"""Integration tests for session expiration handling.

T154: Test session expiration flow
- Expired session → auto redirect to signin
- Graceful logout
"""

from datetime import timedelta

import pytest
from fastapi import status
from httpx import AsyncClient

from src.middleware.auth import create_access_token


class TestSessionExpiration:
    """T154: Integration tests for session expiration handling."""

    @pytest.mark.asyncio
    async def test_expired_token_returns_401(self, client: AsyncClient, registered_user):
        """Test that an expired JWT token is rejected with 401."""
        # Create an expired token (expired 1 hour ago)
        expired_token = create_access_token(
            data={"sub": str(registered_user.id), "email": registered_user.email},
            expires_delta=timedelta(hours=-1),  # Negative delta = expired
        )

        # Try to access protected endpoint with expired token
        response = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {expired_token}"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        error_data = response.json()
        assert "detail" in error_data

    @pytest.mark.asyncio
    async def test_valid_token_within_expiration_succeeds(self, client: AsyncClient, auth_headers):
        """Test that a valid non-expired token works correctly."""
        # Access protected endpoint with valid token
        response = await client.get("/api/v1/auth/me", headers=auth_headers)

        assert response.status_code == status.HTTP_200_OK
        user_data = response.json()
        assert "id" in user_data
        assert "email" in user_data

    @pytest.mark.asyncio
    async def test_token_near_expiration_still_works(self, client: AsyncClient, registered_user):
        """Test that a token close to expiration (but still valid) works."""
        # Create a token that expires in 1 minute
        near_expiration_token = create_access_token(
            data={"sub": str(registered_user.id), "email": registered_user.email}, expires_delta=timedelta(minutes=1)
        )

        # Access protected endpoint
        response = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {near_expiration_token}"})

        assert response.status_code == status.HTTP_200_OK
        user_data = response.json()
        assert user_data["email"] == registered_user.email

    @pytest.mark.asyncio
    async def test_expired_token_cannot_access_tasks(self, client: AsyncClient, registered_user):
        """Test that expired tokens cannot access task endpoints."""
        # Create an expired token
        expired_token = create_access_token(
            data={"sub": str(registered_user.id), "email": registered_user.email}, expires_delta=timedelta(hours=-1)
        )

        # Try to list tasks with expired token
        response = await client.get("/api/v1/tasks", headers={"Authorization": f"Bearer {expired_token}"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_user_can_signin_after_token_expiration(self, client: AsyncClient, registered_user):
        """Test that user can sign in again to get a new token after expiration."""
        # Create an expired token
        expired_token = create_access_token(
            data={"sub": str(registered_user.id), "email": registered_user.email}, expires_delta=timedelta(hours=-1)
        )

        # Verify expired token is rejected
        response = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {expired_token}"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Sign in to get a new token
        signin_response = await client.post(
            "/api/v1/auth/signin", json={"email": "test@example.com", "password": "TestPassword123"}
        )
        assert signin_response.status_code == status.HTTP_200_OK

        # Extract new token
        signin_data = signin_response.json()
        new_token = signin_data["token"]

        # Verify new token works
        me_response = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {new_token}"})
        assert me_response.status_code == status.HTTP_200_OK
        me_data = me_response.json()
        assert me_data["email"] == registered_user.email

    @pytest.mark.asyncio
    async def test_logout_before_expiration_works(self, client: AsyncClient, auth_headers):
        """Test that logout works with a valid (non-expired) token."""
        # Verify token works before logout
        response = await client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK

        # Call logout endpoint
        logout_response = await client.post("/api/v1/auth/logout", headers=auth_headers)
        assert logout_response.status_code == status.HTTP_200_OK
        logout_data = logout_response.json()
        assert "message" in logout_data


class TestSessionManagement:
    """Additional session management tests."""

    @pytest.mark.asyncio
    async def test_malformed_token_returns_401(self, client: AsyncClient):
        """Test that a malformed JWT token is rejected."""
        # Malformed tokens
        malformed_tokens = [
            "not.a.valid.jwt",
            "Bearer invalid_token",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.signature",
            "",
        ]

        for malformed_token in malformed_tokens:
            response = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {malformed_token}"})
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_token_with_invalid_user_id_returns_401(self, client: AsyncClient):
        """Test that a token with a non-existent user ID is rejected."""
        # Create token with invalid user ID
        invalid_token = create_access_token(
            data={"sub": "00000000-0000-0000-0000-000000000000", "email": "nonexistent@example.com"}
        )

        response = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {invalid_token}"})

        # Should return 401 because user doesn't exist
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
