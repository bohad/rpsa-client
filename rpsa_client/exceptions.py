# --- rpsa_client/exceptions.py ---
"""
Custom exceptions thrown by the client.
"""

class APIError(Exception):
    """
    Base exception for API errors.
    """
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(f"HTTP {status_code}: {message}")

class UnauthorizedError(APIError):
    """
    Raised for HTTP 401 Unauthorized.
    """
    pass

class NotFoundError(APIError):
    """
    Raised for HTTP 404 Not Found.
    """
    pass

class BadRequestError(APIError):
    """
    Raised for HTTP 400 Bad Request.
    """
    pass

class RateLimitError(APIError):
    """
    Raised for HTTP 429 Too Many Requests.
    """
    pass