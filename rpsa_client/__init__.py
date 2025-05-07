# --- rpsa_client/__init__.py ---
"""
Package initialization.
"""
from .client import RPSAClient
from .exceptions import (
    APIError,
    UnauthorizedError,
    NotFoundError,
    BadRequestError,
    RateLimitError,
)

__all__ = [
    "RPSAClient",
    "APIError",
    "UnauthorizedError",
    "NotFoundError",
    "BadRequestError",
    "RateLimitError",
]

__version__ = "0.1.0"
