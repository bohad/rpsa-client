# rpsa-client

A Python client library for the RPSA public API.

## Installation

```bash
# Via pip
pip install rpsa-client

# Or with Poetry
poetry add rpsa-client
```

## Quickstart

```python
from rpsa_client import RPSAClient, exceptions

# Initialize the client
client = RPSAClient(
    api_key="YOUR_API_KEY",
    base_url="https://rockpapercode.onespire.hu/api/v1/public"
)

# List arenas
resp = client.list_arenas(page=1, per_page=10)
for arena in resp.data:
    print(arena.id, arena.created_at)

# Get arena details
arena = client.get_arena(arena_id=1)
print(arena)

# Fetch game results
results = client.get_game_results(game_id=42)
for r in results:
    print(r.strategy_name, r.score)

# Strategy summary
summary = client.get_strategy_summary(strategy_id=7)
print(summary.total_score)

# Always close client when done
client.close()
```

## Error handling

- `UnauthorizedError` (401)
- `NotFoundError` (404)
- `BadRequestError` (400)
- `RateLimitError` (429)
- Generic `APIError` for other statuses.

## Testing

```bash
poetry install
poetry run pytest
```
