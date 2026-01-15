"""Integration tests for authentication flows.

T035: Registration flow test
T036: Signin flow test
T037: Session persistence test
"""

import pytest
from fastapi import status
from httpx import AsyncClient


class TestRegistrationFlow:
    """T035: Integration tests for registration flow."""

    @pytest.mark.asyncio
    async def test_registration_flow_success(self, client: AsyncClient):
        """Test complete registration flow with valid data."""
        # Register a new user
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "integration_test@example.com",
                "password": "SecurePassword123!",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()

        # Verify response structure
        assert "user" in data
        assert "token" in data

        # Verify user data
        user = data["user"]
        assert user["email"] == "integration_test@example.com"
        assert "id" in user
        assert "created_at" in user
        assert "updated_at" in user

        # Verify token is a non-empty string
        assert isinstance(data["token"], str)
        assert len(data["token"]) > 0

    @pytest.mark.asyncio
    async def test_registration_validates_email_format(self, client: AsyncClient):
        """Test email validation during registration."""
        invalid_emails = [
            "notanemail",
            "@example.com",
            "user@",
            "user space@example.com",
            "",
        ]

        for invalid_email in invalid_emails:
            response = await client.post(
                "/api/v1/auth/register",
                json={
                    "email": invalid_email,
                    "password": "SecurePassword123!",
                },
            )
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.asyncio
    async def test_registration_validates_password_requirements(self, client: AsyncClient):
        """Test password strength validation during registration."""
        weak_passwords = [
            "short",  # Too short
            "1234567",  # Too short
            "",  # Empty
        ]

        for weak_password in weak_passwords:
            response = await client.post(
                "/api/v1/auth/register",
                json={
                    "email": "test@example.com",
                    "password": weak_password,
                },
            )
            # Should return 400 or 422 for validation errors
            assert response.status_code in [
                status.HTTP_400_BAD_REQUEST,
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            ]

    @pytest.mark.asyncio
    async def test_registration_detects_duplicate_email(self, client: AsyncClient, registered_user):
        """Test duplicate email detection during registration."""
        # Try to register with the same email as registered_user
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",  # Same as registered_user fixture
                "password": "AnotherPassword123!",
            },
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        error_data = response.json()
        assert "detail" in error_data
        assert "already registered" in error_data["detail"].lower()


class TestSigninFlow:
    """T036: Integration tests for signin flow."""

    @pytest.mark.asyncio
    async def test_signin_flow_with_valid_credentials(self, client: AsyncClient, registered_user):
        """Test complete signin flow with valid credentials."""
        # Sign in with valid credentials
        response = await client.post(
            "/api/v1/auth/signin",
            json={
                "email": "test@example.com",
                "password": "TestPassword123",
            },
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Verify response structure
        assert "user" in data
        assert "token" in data

        # Verify user data
        user = data["user"]
        assert user["email"] == "test@example.com"
        assert user["id"] == str(registered_user.id)

        # Verify token is valid
        assert isinstance(data["token"], str)
        assert len(data["token"]) > 0

    @pytest.mark.asyncio
    async def test_signin_fails_with_invalid_password(self, client: AsyncClient, registered_user):
        """Test signin fails with wrong password."""
        response = await client.post(
            "/api/v1/auth/signin",
            json={
                "email": "test@example.com",
                "password": "WrongPassword123!",
            },
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        error_data = response.json()
        assert "detail" in error_data
        assert "invalid" in error_data["detail"].lower()

    @pytest.mark.asyncio
    async def test_signin_fails_with_nonexistent_user(self, client: AsyncClient):
        """Test signin fails with email that doesn't exist."""
        response = await client.post(
            "/api/v1/auth/signin",
            json={
                "email": "nonexistent@example.com",
                "password": "SomePassword123!",
            },
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        error_data = response.json()
        assert "detail" in error_data


class TestSessionPersistence:
    """T037: Integration tests for session persistence."""

    @pytest.mark.asyncio
    async def test_session_token_allows_authenticated_requests(self, client: AsyncClient, auth_headers):
        """Test that session token allows access to protected endpoints."""
        # Access the /me endpoint with valid token
        response = await client.get(
            "/api/v1/auth/me",
            headers=auth_headers,
        )

        assert response.status_code == status.HTTP_200_OK
        user_data = response.json()
        assert "id" in user_data
        assert "email" in user_data
        assert user_data["email"] == "test@example.com"

    @pytest.mark.asyncio
    async def test_invalid_token_rejects_authenticated_requests(self, client: AsyncClient):
        """Test that invalid tokens are rejected."""
        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token_12345"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_missing_token_rejects_authenticated_requests(self, client: AsyncClient):
        """Test that requests without tokens are rejected."""
        response = await client.get("/api/v1/auth/me")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_token_validity_across_multiple_requests(self, client: AsyncClient, auth_headers):
        """Test token remains valid across multiple requests."""
        # Make multiple authenticated requests
        for _ in range(3):
            response = await client.get(
                "/api/v1/auth/me",
                headers=auth_headers,
            )
            assert response.status_code == status.HTTP_200_OK
            user_data = response.json()
            assert user_data["email"] == "test@example.com"

    @pytest.mark.asyncio
    async def test_logout_workflow(self, client: AsyncClient, auth_headers):
        """Test logout invalidates session (client-side for JWT)."""
        # Verify token works before logout
        response = await client.get(
            "/api/v1/auth/me",
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_200_OK

        # Call logout endpoint
        response = await client.post(
            "/api/v1/auth/logout",
            headers=auth_headers,
        )
        assert response.status_code == status.HTTP_200_OK

        # For JWT-based auth, logout is client-side
        # Token technically still valid until expiration
        # This tests the logout endpoint succeeds
        logout_data = response.json()
        assert "message" in logout_data


class TestAuthFlowIntegration:
    """Integration tests combining multiple auth flows."""

    @pytest.mark.asyncio
    async def test_complete_user_journey(self, client: AsyncClient):
        """Test complete user journey: register → signin → access protected resource → logout."""
        # Step 1: Register
        register_response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "journey_user@example.com",
                "password": "JourneyPassword123!",
            },
        )
        assert register_response.status_code == status.HTTP_201_CREATED
        register_data = register_response.json()
        token_from_register = register_data["token"]

        # Step 2: Access protected resource with registration token
        me_response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token_from_register}"},
        )
        assert me_response.status_code == status.HTTP_200_OK
        me_data = me_response.json()
        assert me_data["email"] == "journey_user@example.com"

        # Step 3: Logout
        logout_response = await client.post(
            "/api/v1/auth/logout",
            headers={"Authorization": f"Bearer {token_from_register}"},
        )
        assert logout_response.status_code == status.HTTP_200_OK

        # Step 4: Sign in again
        signin_response = await client.post(
            "/api/v1/auth/signin",
            json={
                "email": "journey_user@example.com",
                "password": "JourneyPassword123!",
            },
        )
        assert signin_response.status_code == status.HTTP_200_OK
        signin_data = signin_response.json()
        new_token = signin_data["token"]

        # Step 5: Access protected resource with new signin token
        me_response_2 = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {new_token}"},
        )
        assert me_response_2.status_code == status.HTTP_200_OK
        me_data_2 = me_response_2.json()
        assert me_data_2["email"] == "journey_user@example.com"
