# --- rpsa_client/models.py ---
"""
Pydantic models mapping API JSON responses to Python objects.
"""
from pydantic import BaseModel, Field
from typing import List, Generic, TypeVar, Optional

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
    is_regular: bool  # ← added
    games_played: int  # ← added
    total_rounds: int  # ← added
    avg_game_runtime: Optional[float]  # ← added


class GameSummary(BaseModel):
    id: int
    game_number: int
    runtime: Optional[float]

    strategy_a_id: int  # ← added
    strategy_b_id: int  # ← added
    wins_a: int  # ← added
    wins_b: int  # ← added
    ties: int  # ← added
    total_rounds: int  # ← added


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
    net_score: int
    win_rate: float
