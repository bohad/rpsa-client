# --- rpsa_client/models.py ---
"""
Pydantic models mapping API JSON responses to Python objects.
"""
from pydantic import BaseModel, Field
from typing import List, Generic, TypeVar, Optional, Dict, Any

T = TypeVar("T")


class Pagination(BaseModel):
    total: int
    page: int
    per_page: int
    pages: int


class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    pagination: Pagination


class Arena(BaseModel):
    id: int
    created_at: str
    number_strategies: int
    rounds_per_game: int
    games_per_pair: int
    max_points: int
    runtime: Optional[float]
    is_regular: bool
    games_played: int
    total_rounds: int
    avg_game_runtime: Optional[float]


class GameSummary(BaseModel):
    id: int
    game_number: int
    runtime: Optional[float]

    strategy_a_id: int
    strategy_b_id: int
    wins_a: int
    wins_b: int
    ties: int
    total_rounds: int


class Result(BaseModel):
    strategy_id: int
    strategy_name: str
    opponent_strategy_id: int

    wins: int
    losses: int
    ties: int
    win_rate: float
    net_score: int
    score: float


class StrategySummary(BaseModel):
    strategy_id: int
    strategy_name: str
    plays: int
    wins: int
    losses: int
    ties: int
    total_score: float
    avg_points_per_game: float
    games_played: int
    net_score: int
    win_rate: float


class LeaderboardEntry(BaseModel):
    strategy_id: int
    strategy_name: str
    avg_points_per_game: float
    games_played: int
    wins: int
    losses: int
    ties: int
    net_score: int
    win_rate: float


class MatchupEntry(BaseModel):
    strategy_id: int
    opponent_strategy_id: int
    wins: int
    losses: int
    ties: int
    net_score: int
    win_rate: float
    avg_points_per_game: float
    games_played: int
