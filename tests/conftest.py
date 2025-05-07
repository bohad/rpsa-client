# --- tests/conftest.py ---
from typing import Generator
import pytest
from pytest_httpx import HTTPXMock


@pytest.fixture
def httpx_mock() -> HTTPXMock:
    """
    Pytest fixture that returns an HTTPXMock instance
    for mocking httpx.Client requests.
    """
    return HTTPXMock()
