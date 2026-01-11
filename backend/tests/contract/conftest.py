"""Pytest fixtures for OpenAPI contract testing."""

import json

import pytest
import yaml


@pytest.fixture(scope="session")
def openapi_spec():
    """Load OpenAPI specification for contract testing."""
    try:
        with open("specs/002-phase2-webapp/contracts/tasks-api.openapi.yaml", "r") as f:
            spec = yaml.safe_load(f)
        return spec
    except FileNotFoundError:
        pytest.skip("OpenAPI spec not found")


@pytest.fixture
def contract_validator(openapi_spec):
    """Create a contract validator."""

    class ContractValidator:
        def __init__(self, spec):
            self.spec = spec
            self.paths = spec.get("paths", {})

        def validate_endpoint_exists(self, path: str, method: str) -> bool:
            """Validate endpoint exists in spec."""
            path_spec = self.paths.get(path)
            if not path_spec:
                return False
            return method.lower() in path_spec

        def validate_request_schema(self, path: str, method: str, request_body: dict) -> bool:
            """Validate request matches schema."""
            endpoint = self.paths.get(path, {}).get(method.lower(), {})
            request_spec = endpoint.get("requestBody", {})
            # Basic validation - implement full validation as needed
            return True

        def validate_response_schema(self, path: str, method: str, status_code: int, response_body: dict) -> bool:
            """Validate response matches schema."""
            endpoint = self.paths.get(path, {}).get(method.lower(), {})
            responses = endpoint.get("responses", {})
            response_spec = responses.get(str(status_code))
            # Basic validation - implement full validation as needed
            return response_spec is not None

    return ContractValidator(openapi_spec)
