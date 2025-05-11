import httpx
from typing import Any, Dict, List

from .exceptions import (
    APIError,
    UnauthorizedError,
    NotFoundError,
    BadRequestError,
    RateLimitError,
)
from .models import (
    Arena,
    PaginatedResponse,
    GameSummary,
    Result,
    StrategySummary,
)


class RPSAClient:
    """
    Client for interacting with the RPSA public API.

    Args:
        api_key: Your API key for authentication.
        base_url: Base URL of the public API (no trailing slash).
        timeout: HTTP request timeout in seconds.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str,
        timeout: float = 120.0,
    ):
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={
                "X-API-KEY": api_key,
                "Accept": "application/json",
            },
            timeout=timeout,
        )

    def _handle_response(self, response: httpx.Response) -> Any:
        code = response.status_code
        if code == 401:
            raise UnauthorizedError(code, response.text)
        if code == 404:
            raise NotFoundError(code, response.text)
        if code == 400:
            raise BadRequestError(code, response.text)
        if code == 429:
            raise RateLimitError(code, response.text)
        if code >= 400:
            raise APIError(code, response.text)
        try:
            return response.json()
        except ValueError:
            raise APIError(code, "Invalid JSON response")

    # ────────────────────────────────────────────────────────────────────────────
    # Arenas
    # ────────────────────────────────────────────────────────────────────────────
    def list_regular_arenas(
        self, page: int = 1, per_page: int = 20
    ) -> PaginatedResponse[Arena]:
        """
        GET /arenas/regular
        Paginated list of *public* (regular) arenas.
        """
        params = {"page": page, "per_page": per_page}
        resp = self._client.get("/arenas/regular", params=params)
        data = self._handle_response(resp)
        return PaginatedResponse[Arena](**data)

    def list_irregular_arenas(
        self, page: int = 1, per_page: int = 20
    ) -> PaginatedResponse[Arena]:
        """
        GET /arenas/irregular
        Paginated list of your private (irregular) arenas.
        """
        params = {"page": page, "per_page": per_page}
        resp = self._client.get("/arenas/irregular", params=params)
        data = self._handle_response(resp)
        return PaginatedResponse[Arena](**data)

    def get_arena(self, arena_id: int) -> Arena:
        """
        GET /arenas/{arena_id}
        Retrieve a single arena's metadata (regular or your own irregular).
        """
        resp = self._client.get(f"/arenas/{arena_id}")
        data = self._handle_response(resp)
        return Arena(**data)

    def list_arena_games(
        self,
        arena_id: int,
        page: int = 1,
        per_page: int = 20,
        sort: str = "game_number,asc",
    ) -> PaginatedResponse[GameSummary]:
        """
        GET /arenas/{arena_id}/games
        List games in an arena with optional sorting.
        """
        params = {"page": page, "per_page": per_page, "sort": sort}
        resp = self._client.get(f"/arenas/{arena_id}/games", params=params)
        data = self._handle_response(resp)
        return PaginatedResponse[GameSummary](**data)

    def get_arena_leaderboard(self, arena_id: int) -> List[Dict[str, Any]]:
        """
        GET /arenas/{arena_id}/leaderboard
        Returns per-arena ranking sorted by average points per game.
        """
        resp = self._client.get(f"/arenas/{arena_id}/leaderboard")
        return self._handle_response(resp)

    def get_arena_matchups(self, arena_id: int) -> List[Dict[str, Any]]:
        """
        GET /arenas/{arena_id}/matchups
        Returns head-to-head aggregates including average points per game.
        """
        resp = self._client.get(f"/arenas/{arena_id}/matchups")
        return self._handle_response(resp)

    # ────────────────────────────────────────────────────────────────────────────
    # Games
    # ────────────────────────────────────────────────────────────────────────────
    def list_regular_games(
        self, page: int = 1, per_page: int = 20, sort: str = "game_number,asc"
    ) -> PaginatedResponse[GameSummary]:
        """
        GET /games/regular
        Paginated list of games from public arenas.
        """
        params = {"page": page, "per_page": per_page, "sort": sort}
        resp = self._client.get("/games/regular", params=params)
        data = self._handle_response(resp)
        return PaginatedResponse[GameSummary](**data)

    def list_irregular_games(
        self, page: int = 1, per_page: int = 20, sort: str = "game_number,asc"
    ) -> PaginatedResponse[GameSummary]:
        """
        GET /games/irregular
        Paginated list of games from your private arenas.
        """
        params = {"page": page, "per_page": per_page, "sort": sort}
        resp = self._client.get("/games/irregular", params=params)
        data = self._handle_response(resp)
        return PaginatedResponse[GameSummary](**data)

    def get_game_results(self, game_id: int) -> List[Result]:
        """
        GET /games/{game_id}
        Fetch all result records for a specific game.
        """
        resp = self._client.get(f"/games/{game_id}")
        data = self._handle_response(resp)
        return [Result(**item) for item in data]

    # ────────────────────────────────────────────────────────────────────────────
    # Strategies
    # ────────────────────────────────────────────────────────────────────────────
    def list_regular_strategies(
        self, page: int = 1, per_page: int = 20, sort: str = "avg_ppg,desc"
    ) -> PaginatedResponse[StrategySummary]:
        """
        GET /strategies/regular
        Paginated list of public strategies with avg points/game.
        """
        params = {"page": page, "per_page": per_page, "sort": sort}
        resp = self._client.get("/strategies/regular", params=params)
        data = self._handle_response(resp)
        return PaginatedResponse[StrategySummary](**data)

    def list_irregular_strategies(
        self, page: int = 1, per_page: int = 20, sort: str = "avg_ppg,desc"
    ) -> PaginatedResponse[StrategySummary]:
        """
        GET /strategies/irregular
        Paginated list of your private strategies with avg points/game.
        """
        params = {"page": page, "per_page": per_page, "sort": sort}
        resp = self._client.get("/strategies/irregular", params=params)
        data = self._handle_response(resp)
        return PaginatedResponse[StrategySummary](**data)

    def get_strategy_summary(self, strategy_id: int) -> StrategySummary:
        """
        GET /strategies/{strategy_id}/results
        Retrieve aggregated performance for a strategy.
        """
        resp = self._client.get(f"/strategies/{strategy_id}/results")
        data = self._handle_response(resp)
        return StrategySummary(**data)

    def get_strategy_head_to_head(self, strategy_id: int) -> List[Dict[str, Any]]:
        """
        GET /strategies/{strategy_id}/head_to_head
        Returns per-opponent aggregates including avg points/game.
        """
        resp = self._client.get(f"/strategies/{strategy_id}/head_to_head")
        return self._handle_response(resp)

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
