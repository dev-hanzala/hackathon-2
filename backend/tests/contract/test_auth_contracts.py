"""Contract tests for authentication endpoints against OpenAPI schema.

T032: Validate /api/v1/auth/register endpoint against OpenAPI schema
T033: Validate /api/v1/auth/signin endpoint against OpenAPI schema
T034: Validate /api/v1/auth/logout endpoint against OpenAPI schema
"""

import pytest
from fastapi import status
from httpx import AsyncClient


class TestRegisterContract:
    """T032: Contract tests for /api/v1/auth/register endpoint."""

    @pytest.mark.asyncio
    async def test_register_success_returns_201(self, client: AsyncClient):
        """Register success returns 201 with user object."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "SecurePassword123",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED

        data = response.json()
        assert "user" in data
        assert "token" in data
        assert "id" in data["user"]
        assert "email" in data["user"]
        assert data["user"]["email"] == "newuser@example.com"
        assert "created_at" in data["user"]

    @pytest.mark.asyncio
    async def test_register_invalid_email_returns_400(self, client: AsyncClient):
        """Register with invalid email format returns 400."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "invalid-email",
                "password": "SecurePassword123",
            },
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_register_short_password_returns_400(self, client: AsyncClient):
        """Register with password < 8 chars returns 400/422."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "short",
            },
        )
        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ]

    @pytest.mark.asyncio
    async def test_register_duplicate_email_returns_409(self, client: AsyncClient, registered_user):
        """Register with existing email returns 409."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",  # Same as registered_user
                "password": "AnotherPassword123",
            },
        )
        assert response.status_code == status.HTTP_409_CONFLICT

    @pytest.mark.asyncio
    async def test_register_missing_fields_returns_422(self, client: AsyncClient):
        """Register with missing required fields returns 422."""
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "test@example.com"},  # Missing password
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestSigninContract:
    """T033: Contract tests for /api/v1/auth/signin endpoint."""

    @pytest.mark.asyncio
    async def test_signin_success_returns_200(self, client: AsyncClient, registered_user):
        """Signin with valid credentials returns 200 with token."""
        response = await client.post(
            "/api/v1/auth/signin",
            json={
                "email": "test@example.com",
                "password": "TestPassword123",
            },
        )
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert "user" in data
        assert "token" in data
        assert "id" in data["user"]
        assert "email" in data["user"]
        assert data["user"]["email"] == "test@example.com"

    @pytest.mark.asyncio
    async def test_signin_invalid_credentials_returns_401(self, client: AsyncClient, registered_user):
        """Signin with wrong password returns 401."""
        response = await client.post(
            "/api/v1/auth/signin",
            json={
                "email": "test@example.com",
                "password": "WrongPassword",
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_signin_nonexistent_user_returns_401(self, client: AsyncClient):
        """Signin with nonexistent user returns 401."""
        response = await client.post(
            "/api/v1/auth/signin",
            json={
                "email": "nonexistent@example.com",
                "password": "SomePassword123",
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_signin_missing_fields_returns_422(self, client: AsyncClient):
        """Signin with missing fields returns 422."""
        response = await client.post(
            "/api/v1/auth/signin",
            json={"email": "test@example.com"},  # Missing password
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestLogoutContract:
    """T034: Contract tests for /api/v1/auth/logout endpoint."""

    @pytest.mark.asyncio
    async def test_logout_success_returns_200(self, client: AsyncClient, auth_headers):
        """Logout with valid session returns 200."""
        response = await client.post(
            "/api/v1/auth/logout",
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_logout_unauthenticated_returns_401(self, client: AsyncClient):
        """Logout without auth token returns 401."""
        response = await client.post("/api/v1/auth/logout")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_logout_invalid_token_returns_401(self, client: AsyncClient):
        """Logout with invalid token returns 401."""
        response = await client.post(
            "/api/v1/auth/logout",
            headers={"Authorization": "Bearer invalid-token"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
