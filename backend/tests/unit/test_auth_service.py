"""Unit tests for auth_service.py (T162).

Tests authentication service methods with mocked database calls.
Focus on business logic without database dependencies.
"""

from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, Mock, patch
from uuid import uuid4

import pytest
from fastapi import HTTPException

from src.db.models import User
from src.services.auth_service import AuthService


class TestAuthServiceRegister:
    """Unit tests for user registration logic."""

    def test_register_user_success(self):
        """Test successful user registration."""
        # Arrange
        mock_db = Mock()
        email = "newuser@example.com"
        password = "SecurePass123!"
        user_id = uuid4()

        # Mock DBService methods
        with (
            patch("src.services.auth_service.DBService") as MockDBService,
            patch("src.services.auth_service.get_password_hash") as mock_hash,
            patch("src.services.auth_service.create_access_token") as mock_token,
        ):
            MockDBService.get_user_by_email.return_value = None  # User doesn't exist
            mock_hash.return_value = "hashed_password_value"

            mock_user = User(
                id=user_id,
                email=email,
                password_hash="hashed_password_value",
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
            )
            MockDBService.create_user.return_value = mock_user
            mock_token.return_value = "jwt_token_123"

            # Act
            user, token = AuthService.register_user(mock_db, email, password)

            # Assert
            assert user.email == email
            assert user.id == user_id
            assert token == "jwt_token_123"
            MockDBService.get_user_by_email.assert_called_once_with(mock_db, email)
            mock_hash.assert_called_once_with(password)
            MockDBService.create_user.assert_called_once_with(mock_db, email, "hashed_password_value")
            mock_token.assert_called_once()

    def test_register_user_duplicate_email(self):
        """Test registration fails when email already exists."""
        # Arrange
        mock_db = Mock()
        email = "existing@example.com"
        password = "SecurePass123!"

        existing_user = User(
            id=uuid4(),
            email=email,
            password_hash="old_hash",
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

        with patch("src.services.auth_service.DBService") as MockDBService:
            MockDBService.get_user_by_email.return_value = existing_user

            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                AuthService.register_user(mock_db, email, password)

            assert exc_info.value.status_code == 409
            assert "already registered" in exc_info.value.detail.lower()
            MockDBService.create_user.assert_not_called()


class TestAuthServiceAuthenticate:
    """Unit tests for user authentication logic."""

    def test_authenticate_user_success(self):
        """Test successful user authentication."""
        # Arrange
        mock_db = Mock()
        email = "user@example.com"
        password = "CorrectPassword123"
        user_id = uuid4()

        mock_user = User(
            id=user_id,
            email=email,
            password_hash="hashed_password",
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

        with (
            patch("src.services.auth_service.DBService") as MockDBService,
            patch("src.services.auth_service.verify_password") as mock_verify,
            patch("src.services.auth_service.create_access_token") as mock_token,
        ):
            MockDBService.get_user_by_email.return_value = mock_user
            mock_verify.return_value = True
            mock_token.return_value = "jwt_token_456"

            # Act
            user, token = AuthService.authenticate_user(mock_db, email, password)

            # Assert
            assert user.id == user_id
            assert user.email == email
            assert token == "jwt_token_456"
            MockDBService.get_user_by_email.assert_called_once_with(mock_db, email)
            mock_verify.assert_called_once_with(password, "hashed_password")
            mock_token.assert_called_once()

    def test_authenticate_user_not_found(self):
        """Test authentication fails when user doesn't exist."""
        # Arrange
        mock_db = Mock()
        email = "nonexistent@example.com"
        password = "SomePassword"

        with patch("src.services.auth_service.DBService") as MockDBService:
            MockDBService.get_user_by_email.return_value = None

            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                AuthService.authenticate_user(mock_db, email, password)

            assert exc_info.value.status_code == 401
            assert "invalid" in exc_info.value.detail.lower()

    def test_authenticate_user_wrong_password(self):
        """Test authentication fails with incorrect password."""
        # Arrange
        mock_db = Mock()
        email = "user@example.com"
        password = "WrongPassword"

        mock_user = User(
            id=uuid4(),
            email=email,
            password_hash="correct_hash",
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

        with (
            patch("src.services.auth_service.DBService") as MockDBService,
            patch("src.services.auth_service.verify_password") as mock_verify,
        ):
            MockDBService.get_user_by_email.return_value = mock_user
            mock_verify.return_value = False  # Password doesn't match

            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                AuthService.authenticate_user(mock_db, email, password)

            assert exc_info.value.status_code == 401
            assert "invalid" in exc_info.value.detail.lower()


class TestAuthServiceTokenValidation:
    """Unit tests for token validation logic."""

    def test_validate_token_success(self):
        """Test successful token validation."""
        # Arrange
        token = "valid_jwt_token"
        expected_payload = {"sub": str(uuid4()), "email": "user@example.com"}

        with patch("src.services.auth_service.decode_access_token") as mock_decode:
            mock_decode.return_value = expected_payload

            # Act
            payload = AuthService.validate_token(token)

            # Assert
            assert payload == expected_payload
            mock_decode.assert_called_once_with(token)

    def test_validate_token_invalid(self):
        """Test validation fails for invalid token."""
        # Arrange
        token = "invalid_token"

        with patch("src.services.auth_service.decode_access_token") as mock_decode:
            mock_decode.return_value = None

            # Act
            payload = AuthService.validate_token(token)

            # Assert
            assert payload is None
            mock_decode.assert_called_once_with(token)


class TestAuthServiceGetUserFromToken:
    """Unit tests for getting user from JWT token."""

    def test_get_user_from_token_success(self):
        """Test successfully retrieving user from valid token."""
        # Arrange
        mock_db = Mock()
        token = "valid_token"
        user_id = uuid4()

        mock_user = User(
            id=user_id,
            email="user@example.com",
            password_hash="hash",
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

        with (
            patch("src.services.auth_service.decode_access_token") as mock_decode,
            patch("src.services.auth_service.DBService") as MockDBService,
        ):
            mock_decode.return_value = {"sub": str(user_id), "email": "user@example.com"}
            MockDBService.get_user_by_id.return_value = mock_user

            # Act
            user = AuthService.get_user_from_token(mock_db, token)

            # Assert
            assert user is not None
            assert user.id == user_id
            MockDBService.get_user_by_id.assert_called_once_with(mock_db, user_id)

    def test_get_user_from_token_invalid_token(self):
        """Test returns None for invalid token."""
        # Arrange
        mock_db = Mock()
        token = "invalid_token"

        with patch("src.services.auth_service.decode_access_token") as mock_decode:
            mock_decode.return_value = None

            # Act
            user = AuthService.get_user_from_token(mock_db, token)

            # Assert
            assert user is None

    def test_get_user_from_token_missing_sub(self):
        """Test returns None when token payload missing 'sub' field."""
        # Arrange
        mock_db = Mock()
        token = "token_without_sub"

        with patch("src.services.auth_service.decode_access_token") as mock_decode:
            mock_decode.return_value = {"email": "user@example.com"}  # No 'sub'

            # Act
            user = AuthService.get_user_from_token(mock_db, token)

            # Assert
            assert user is None

    def test_get_user_from_token_invalid_uuid(self):
        """Test returns None when 'sub' is not a valid UUID."""
        # Arrange
        mock_db = Mock()
        token = "token_with_bad_uuid"

        with patch("src.services.auth_service.decode_access_token") as mock_decode:
            mock_decode.return_value = {"sub": "not-a-valid-uuid"}

            # Act
            user = AuthService.get_user_from_token(mock_db, token)

            # Assert
            assert user is None

    def test_get_user_from_token_user_not_found(self):
        """Test returns None when user doesn't exist in database."""
        # Arrange
        mock_db = Mock()
        token = "token_for_deleted_user"
        user_id = uuid4()

        with (
            patch("src.services.auth_service.decode_access_token") as mock_decode,
            patch("src.services.auth_service.DBService") as MockDBService,
        ):
            mock_decode.return_value = {"sub": str(user_id)}
            MockDBService.get_user_by_id.return_value = None  # User doesn't exist

            # Act
            user = AuthService.get_user_from_token(mock_db, token)

            # Assert
            assert user is None


class TestAuthServiceSessionManagement:
    """Unit tests for session creation and deletion."""

    def test_create_session_success(self):
        """Test successful session creation."""
        # Arrange
        mock_db = Mock()
        user_id = uuid4()

        with (
            patch("src.services.auth_service.DBService") as MockDBService,
            patch("src.services.auth_service.create_access_token") as mock_token,
        ):
            mock_token.return_value = "session_token_789"
            mock_session = MagicMock()
            mock_session.id = uuid4()
            MockDBService.create_session.return_value = mock_session

            # Act
            session = AuthService.create_session(mock_db, user_id)

            # Assert
            assert session.id is not None
            MockDBService.create_session.assert_called_once()
            mock_token.assert_called_once()

    def test_create_session_with_custom_expiry(self):
        """Test session creation with custom expiration."""
        # Arrange
        mock_db = Mock()
        user_id = uuid4()
        custom_delta = timedelta(hours=24)

        with (
            patch("src.services.auth_service.DBService") as MockDBService,
            patch("src.services.auth_service.create_access_token") as mock_token,
        ):
            mock_token.return_value = "long_lived_token"
            mock_session = MagicMock()
            mock_session.id = uuid4()
            MockDBService.create_session.return_value = mock_session

            # Act
            session = AuthService.create_session(mock_db, user_id, expires_delta=custom_delta)

            # Assert
            assert session.id is not None
            MockDBService.create_session.assert_called_once()
            # Verify custom delta was used
            call_args = mock_token.call_args
            assert call_args[1]["expires_delta"] == custom_delta

    def test_delete_session_success(self):
        """Test successful session deletion."""
        # Arrange
        mock_db = Mock()
        token = "session_token_to_delete"

        with patch("src.services.auth_service.DBService") as MockDBService:
            # Act
            AuthService.delete_session(mock_db, token)

            # Assert
            MockDBService.delete_session.assert_called_once_with(mock_db, token)


class TestAuthServiceLogout:
    """Unit tests for logout functionality."""

    def test_logout_user(self):
        """Test logout (JWT-based, mostly no-op on backend)."""
        # Arrange
        mock_db = Mock()
        token = "user_token"

        # Act
        result = AuthService.logout_user(mock_db, token)

        # Assert
        assert result is None  # Logout is client-side for JWT
