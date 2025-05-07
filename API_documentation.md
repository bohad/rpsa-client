# rpsa-client 🪨📄✂️ &nbsp;— Developer Guide

A typed Python SDK for the **Rock-Paper-Scissors Arena** public API  
(built on **httpx** + **pydantic**).

---

## 1 Installation

```bash
pip install rpsa-client        # or: poetry add rpsa-client
```

**Requires Python ≥ 3.9**

## 2 Authentication

Every request needs an API key in the `X-API-KEY` header.

```python
from rpsa_client import RPSAClient

client = RPSAClient(
    api_key="YOUR_32_CHAR_KEY",
    base_url="https://rockpapercode.onespire.hu/api/v1/public"
)
```

```bash
export RPSA_API_KEY=YOUR_32_CHAR_KEY
```

```python
client = RPSAClient(base_url="https://rockpapercode.onespire.hu/api/v1/public")
```

If no key is found, the SDK raises ValueError.

## Quick start

```python
from rpsa_client import RPSAClient

with RPSAClient(api_key="YOUR_KEY",
                base_url="https://rockpapercode.onespire.hu/api/v1/public") as client:

    # 1. list arenas
    arenas_page1 = client.list_arenas(page=1, per_page=5)

    # 2. single arena
    arena = client.get_arena(arenas_page1.data[0].id)

    # 3. games in that arena
    games = client.list_games(arena.id)

    # 4. full results for one game
    results = client.get_game_results(games.data[0].id)

    # 5. aggregate stats for a strategy
    summary = client.get_strategy_summary(strategy_id=results[0].strategy_id)
```

All return values are **pydantic models** with IDE autocompletion.

## 4 Endpoint Reference & Schemas

### 4.1 List Arenas `GET /arenas`

Get information about all arenas.

#### Query Parameters

| Name       | Type | Default             | Description                                  |
| ---------- | ---- | ------------------- | -------------------------------------------- |
| `page`     | int  | `1`                 | Page number (must be ≥ 1)                    |
| `per_page` | int  | `10`                | Items per page (must be between 1 and 100)   |
| `sort`     | str  | `"created_at,desc"` | Sorting field and direction (e.g., `id,asc`) |

---

#### Usage example

```python
from rpsa_client import RPSAClient
client = RPSAClient(api_key="your_api_key")
arena = client.list_arenas(page=1, per_page = 10, sort = "created_at, asc")
```

---

#### Response – `200 OK`

```json
{
  "data": [
    {
      "id": 42,
      "created_at": "2025-04-20T14:32:10Z",
      "number_strategies": 5,
      "rounds_per_game": 2000,
      "games_per_pair": 100,
      "max_points": 100,
      "is_regular": true,
      "games_played": 500,
      "total_rounds": 1000000,
      "avg_game_runtime": 0.025
    }
  ],
  "pagination": {
    "total": 12,
    "page": 1,
    "per_page": 10,
    "pages": 2
  }
}
```

#### Response Fields – `data[]`

| Field               | Type    | Description                                              |
| ------------------- | ------- | -------------------------------------------------------- |
| `id`                | int     | Unique identifier of the arena                           |
| `created_at`        | string  | ISO 8601 formatted timestamp when the arena was created  |
| `number_strategies` | int     | Total number of strategies that participated             |
| `rounds_per_game`   | int     | Number of rounds played in each game                     |
| `games_per_pair`    | int     | Number of games played between each pair of strategies   |
| `max_points`        | int     | Maximum number of points awarded in each game            |
| `is_regular`        | boolean | Whether the arena is a regular match (`true` or `false`) |
| `games_played`      | int     | Total games recorded                                     |
| `total_rounds`      | int     | Total rounds played                                      |
| `avg_game_runtime`  | float   | Time taken to complete the arena execution (in seconds)  |

#### Pagination object

| Field      | Type | Description                                                             |
| ---------- | ---- | ----------------------------------------------------------------------- |
| `page`     | int  | Current page number                                                     |
| `per_page` | int  | Number of items returned per page                                       |
| `total`    | int  | Total number of items matching the query criteria                       |
| `pages`    | int  | Total number of pages available based on the current `per_page` setting |

### 4.2 Get Single Arena `GET /arenas/{arena_id}`

Retrieve the detailed information of a specific arena by its ID.

#### Query Parameters

| Name       | Type | Default | Description |
| ---------- | ---- | ------- | ----------- |
| `arena_id` | int  | `1`     | Arena Id    |

#### Usage example

```python
from rpsa_client import RPSAClient
client = RPSAClient(api_key="your_api_key")
arena = client.get_arena(arena_id=3)
```

#### Response – `200 OK`

```json
{
  "id": 42,
  "created_at": "2025-04-20T14:32:10Z",
  "number_strategies": 5,
  "rounds_per_game": 2000,
  "games_per_pair": 100,
  "max_points": 100,
  "is_regular": true,
  "games_played": 500,
  "total_rounds": 1000000,
  "avg_game_runtime": 0.025,
  "runtime": 12.345
}
```

#### Response Field

| Field               | Type   | Description                                             |
| ------------------- | ------ | ------------------------------------------------------- |
| `id`                | int    | The unique ID of the arena                              |
| `created_at`        | string | ISO 8601 formatted timestamp when the arena was created |
| `number_strategies` | int    | Number of strategies that participated in the arena     |
| `rounds_per_game`   | int    | Number of rounds per game                               |
| `games_per_pair`    | int    | Number of games played between each strategy pair       |
| `max_points`        | int    | Maximum points that can be earned per game              |
| `is_regular`        | bool   | Whether the arena is part of regular competition        |
| `games_played`      | int    | Total games recorded                                    |
| `total_rounds`      | int    | Total rounds played                                     |
| `avg_game_runtime`  | float  | Average runtime per game                                |
| `runtime`           | float  | Time taken to complete the arena execution (in seconds) |

### 4.3 List Games in Arena `GET /arenas/{arena_id}/games`

#### Path Parameters

| Name       | Type | Default | Description |
| ---------- | ---- | ------- | ----------- |
| `arena_id` | int  | `1`     | Arena Id    |

#### Query Parameters

| Name       | Type | Default           | Description                                |
| ---------- | ---- | ----------------- | ------------------------------------------ |
| `page`     | int  | `1`               | Page number (must be ≥ 1)                  |
| `per_page` | int  | `10`              | Items per page (must be between 1 and 100) |
| `sort`     | str  | `game_number,asc` | `game_number` only                         |

#### Usage example

```python
from rpsa_client import RPSAClient
client = RPSAClient(api_key="your_api_key")
games = client.list_games(page=1, per_page = 10, sort = "created_at, asc")
```

#### Response – `200 OK`

```json
{
  "data": [
    {
      "id": 101,
      "game_number": 1,
      "runtime": 0.032,
      "strategy_a_id": 7,
      "strategy_b_id": 3,
      "wins_a": 1020,
      "wins_b": 980,
      "ties": 0,
      "total_rounds": 2000
    }
  ],
  "pagination": {
    "total": 200,
    "page": 1,
    "per_page": 5,
    "pages": 40
  }
}
```

#### Response fields

| Field           | Type   | Description                                          |
| --------------- | ------ | ---------------------------------------------------- |
| `id`            | int    | Game Id                                              |
| `game_number`   | int    | Index of this game in the arena run                  |
| `runtime`       | number | Time to play this game (in seconds)                  |
| `strategy_a_id` | int    | Database ID of the first strategy                    |
| `strategy_b_id` | int    | Database ID of the second strategy                   |
| `wins_a`        | number | Number of wins by strategy A                         |
| `wins_b`        | int    | Number of wins by strategy B                         |
| `ties`          | int    | Number of ties                                       |
| `total_rounds`  | number | Total rounds played (should equal `rounds_per_game`) |

### 4.4 Get Arena Leaderboard `GET /arenas/{arena_id}/leaderboard`

Get per-strategy ranking for an arena.

#### Path Parameters

| Name       | Type | Default | Description |
| ---------- | ---- | ------- | ----------- |
| `arena_id` | int  | `1`     | Arena Id    |

#### Usage example

```python
from rpsa_client import RPSAClient
client = RPSAClient(api_key="your_api_key")
games = client.get_arena_leaderboard(game_id = 42)
```

#### Response - `200 OK`

```json
[
  {
    "strategy_id": 7,
    "strategy_name": "RockMaster",
    "total_score": 12.5,
    "wins": 50,
    "losses": 30,
    "ties": 20,
    "net_score": 20,
    "win_rate": 0.625
  },
  {
    "strategy_id": 3,
    "strategy_name": "PaperPro",
    "total_score": 10.0,
    "wins": 45,
    "losses": 35,
    "ties": 20,
    "net_score": 10,
    "win_rate": 0.5625
  },
  ...
]
```

#### Response fields

| Field           | Type  | Description                                               |
| --------------- | ----- | --------------------------------------------------------- |
| `strategy_id`   | int   | Strategy in focus                                         |
| `strategy_name` | str   | Public strategy name                                      |
| `total_score`   | float | Sum of all normalized game‐scores across the entire arena |
| `wins`          | int   | Total number of games won by this strategy                |
| `losses`        | int   | Total number of games lost by this strategy               |
| `ties`          | int   | Total number of games that resulted in a tie              |
| `net_score`     | int   | `wins - losses`                                           |
| `win_rate`      | float | `wins / (wins + losses)`, rounded to 4 decimal places     |

### 4.5 Get Arena Matchups `GET /arenas/{arena_id}/matchups`

Get per-strategy ranking for an arena.

#### Path Parameters

| Name       | Type | Default | Description |
| ---------- | ---- | ------- | ----------- |
| `arena_id` | int  | `1`     | Arena Id    |

#### Usage example

```python
from rpsa_client import RPSAClient
client = RPSAClient(api_key="your_api_key")
matchups = client.get_arena_matchups(arena_id=42)
```

#### Response - `200 OK`

```json
[
  {
    "strategy_id": 7,
    "opponent_strategy_id": 3,
    "wins": 30,
    "losses": 20,
    "ties": 0,
    "net_score": 10,
    "win_rate": 0.6000,
    "avg_points_per_game": 0.1500
  },
  {
    "strategy_id": 7,
    "opponent_strategy_id": 5,
    "wins": 25,
    "losses": 25,
    "ties": 0,
    "net_score": 0,
    "win_rate": 0.5000,
    "avg_points_per_game": 0.0500
  },
  {
    "strategy_id": 7,
    "opponent_strategy_id": 9,
    "wins": 35,
    "losses": 15,
    "ties": 0,
    "net_score": 20,
    "win_rate": 0.7000,
    "avg_points_per_game": 0.2000
  },
  ...
]
```

#### Response fields

| Field                  | Type  | Description                                                                  |
| ---------------------- | ----- | ---------------------------------------------------------------------------- |
| `strategy_id`          | int   | Strategy in focus                                                            |
| `opponent_strategy_id` | int   | Public strategy name                                                         |
| `wins`                 | int   | Total number of games won by this strategy                                   |
| `losses`               | int   | Total number of games lost by this strategy                                  |
| `ties`                 | int   | Total number of games that resulted in a tie                                 |
| `net_score`            | int   | `wins - losses`                                                              |
| `win_rate`             | float | `wins / (wins + losses)`, rounded to 4 decimal places                        |
| `avg_points_per_game`  | float | Average of the normalized `score` field for each game, rounded to 4 decimals |

### 4.6 List Games `GET /games`

Get a paginated list of all visible games.

#### Query Parameters

| Name       | Type | Default           | Description                                |
| ---------- | ---- | ----------------- | ------------------------------------------ |
| `page`     | int  | `1`               | Page number (must be ≥ 1)                  |
| `per_page` | int  | `10`              | Items per page (must be between 1 and 100) |
| `sort`     | str  | `game_number,asc` | `game_number` only                         |

#### Usage example

```python
from rpsa_client import RPSAClient
client = RPSAClient(api_key="your_api_key")
games = client.list_games(page=1, per_page=5, sort="runtime,asc")
```

#### Response - `200 OK`

```json
{
  "data": [
    {
      "id": 101,
      "game_number": 1,
      "runtime": 0.032,
      "strategy_a_id": 7,
      "strategy_b_id": 3,
      "wins_a": 1020,
      "wins_b": 980,
      "ties": 0,
      "total_rounds": 2000
    },
    {
      "id": 102,
      "game_number": 2,
      "runtime": 0.028,
      "strategy_a_id": 7,
      "strategy_b_id": 5,
      "wins_a": 1100,
      "wins_b": 900,
      "ties": 0,
      "total_rounds": 2000
    },
    {
      "id": 103,
      "game_number": 3,
      "runtime": 0.035,
      "strategy_a_id": 3,
      "strategy_b_id": 9,
      "wins_a": 950,
      "wins_b": 1050,
      "ties": 0,
      "total_rounds": 2000
    },
    ...
  ],
  "pagination": {
    "total": 500,
    "page": 1,
    "per_page": 5,
    "pages": 100
  }
}
```

#### Response fields

| Field           | Type  | Description                                               |
| --------------- | ----- | --------------------------------------------------------- |
| `id`            | int   | Unique identifier of the game                             |
| `game_number`   | int   | Sequential index of this game within its arena run        |
| `runtime`       | float | Time taken to execute this game (in seconds)              |
| `strategy_a_id` | int   | Database ID of the first (home) strategy                  |
| `strategy_b_id` | int   | Database ID of the second (away) strategy                 |
| `wins_a`        | int   | Number of rounds won by `strategy_a`                      |
| `wins_b`        | int   | Number of rounds won by `strategy_b`                      |
| `ties`          | float | Number of tied rounds                                     |
| `total_rounds`  | float | Total rounds played (equals configured `rounds_per_game`) |

### 4.7 Get Game Results `GET /games/{game_id}`

#### Path Parameters

| Name      | Type | Default | Description |
| --------- | ---- | ------- | ----------- |
| `game_id` | int  | `1`     | Game Id     |

#### Usage example

```python
from rpsa_client import RPSAClient
client = RPSAClient(api_key="your_api_key")
games = client.get_game_results(game_id = 51)
```

#### Response - `200 OK`

```json
[
  {
    "strategy_id": 7,
    "strategy_name": "RockMaster",
    "opponent_strategy_id": 3,
    "wins": 1020,
    "losses": 980,
    "ties": 0,
    "win_rate": 0.51,
    "net_score": 40,
    "score": 0.04
  },
  {
    "strategy_id": 3,
    "strategy_name": "PaperPro",
    "opponent_strategy_id": 7,
    "wins": 980,
    "losses": 1020,
    "ties": 0,
    "win_rate": 0.49,
    "net_score": -40,
    "score": -0.04
  }
]
```

#### Response fields

| Field                  | Type   | Description                                                                 |
| ---------------------- | ------ | --------------------------------------------------------------------------- |
| `strategy_id`          | int    | ID of the strategy                                                          |
| `strategy_name`        | str    | Public strategy name                                                        |
| `opponent_strategy_id` | int    | ID of the opposing strategy in this game                                    |
| `wins`                 | str    | Number of rounds this strategy won                                          |
| `losses`               | number | Number of rounds this strategy lost                                         |
| `ties`                 | number | Number of rounds that ended in a tie                                        |
| `win_rate`             | number | `wins / (wins + losses)`, rounded to 4 decimal places                       |
| `net_score`            | number | Difference `wins - losses`                                                  |
| `score`                | number | Normalized, signed game‐score for this strategy (e.g. between -1.0 and 1.0) |

### 4.8 List strategies `GET /strategies`

#### Query Parameters

| Name       | Type | Default           | Description                                |
| ---------- | ---- | ----------------- | ------------------------------------------ |
| `page`     | int  | `1`               | Page number (must be ≥ 1)                  |
| `per_page` | int  | `10`              | Items per page (must be between 1 and 100) |
| `sort`     | str  | `game_number,asc` | `game_number` only                         |

#### Usage example

```python
from rpsa_client import RPSAClient
client = RPSAClient(api_key="your_api_key")
strategies = client.list_strategies(page=1, per_page=10, sort="total_score,desc")
```

#### Response - `200 OK`

```json
{
  "data": [
    {
      "strategy_id": 7,
      "strategy_name": "RockMaster",
      "plays": 1000,
      "wins": 600,
      "losses": 300,
      "ties": 100,
      "total_score": 50.0,
      "net_score": 300,
      "win_rate": 0.6
    },
    {
      "strategy_id": 3,
      "strategy_name": "PaperPro",
      "plays": 950,
      "wins": 550,
      "losses": 300,
      "ties": 100,
      "total_score": 45.0,
      "net_score": 250,
      "win_rate": 0.6474
    },
    {
      "strategy_id": 5,
      "strategy_name": "ScissorSage",
      "plays": 900,
      "wins": 450,
      "losses": 350,
      "ties": 100,
      "total_score": 40.0,
      "net_score": 100,
      "win_rate": 0.5625
    },
    ...
  ],
  "pagination": {
    "total": 50,
    "page": 1,
    "per_page": 10,
    "pages": 5
  }
}
```

#### Response fields

| Field           | Type  | Description                                           |
| --------------- | ----- | ----------------------------------------------------- |
| `strategy_id`   | int   | Unique identifier of the strategy                     |
| `strategy_name` | int   | Human‐readable name/module of the strategy            |
| `plays`         | float | Total number of games played                          |
| `wins`          | int   | Total number of games won                             |
| `losses`        | int   | Total number of games lost                            |
| `ties`          | int   | Total number of tied games                            |
| `total_score`   | int   | Sum of normalized game‐scores across all games        |
| `net_score`     | float | Difference `wins − losses`                            |
| `win_rate`      | float | `wins / (wins + losses)`, rounded to 4 decimal places |

### 4.9 Get Strategy Summary `GET /strategies/{strategy_id}/results`

#### Path Parameters

| Name          | Type | Default | Description |
| ------------- | ---- | ------- | ----------- |
| `strategy_id` | int  | `1`     | Strategy Id |

#### Usage example

```python
from rpsa_client import RPSAClient
client = RPSAClient(api_key="your_api_key")
summary = client.get_strategy_summary(strategy_id=7)
```

#### Response - `200 OK`

```json
{
  "strategy_id": 7,
  "strategy_name": "RockMaster",
  "plays": 1000,
  "wins": 600,
  "losses": 300,
  "ties": 100,
  "total_score": 50.0,
  "net_score": 300,
  "win_rate": 0.6667
}
```

#### Response fields

| Field           | Type  | Description                                           |
| --------------- | ----- | ----------------------------------------------------- |
| `strategy_id`   | int   | Strategy ID                                           |
| `strategy_name` | int   | Human‐readable name/module of the strategy            |
| `plays`         | float | Total number of games played                          |
| `wins`          | int   | Total number of games won                             |
| `losses`        | int   | Total number of games lost                            |
| `ties`          | int   | Total number of tied games                            |
| `total_score`   | int   | Sum of normalized game‐scores across all games        |
| `net_score`     | float | Difference `wins − losses`                            |
| `win_rate`      | float | `wins / (wins + losses)`, rounded to 4 decimal places |

### 4.10 Get Strategy Head-to-Head `GET /strategies/{strategy_id}/head_to_head`

Get per-opponent performance metrics for one strategy.

#### Path Parameters

| Name          | Type | Default | Description |
| ------------- | ---- | ------- | ----------- |
| `strategy_id` | int  | `1`     | Strategy Id |

#### Usage example

```python
from rpsa_client import RPSAClient
client = RPSAClient(api_key="your_api_key")
h2h = client.get_strategy_head_to_head(strategy_id=7)
```

#### Response - `200 OK`

```json
[
  {
    "strategy_id": 7,
    "opponent_strategy_id": 3,
    "wins": 30,
    "losses": 20,
    "ties": 0,
    "net_score": 10,
    "win_rate": 0.6,
    "avg_points_per_game": 0.15
  },
  {
    "strategy_id": 7,
    "opponent_strategy_id": 5,
    "wins": 25,
    "losses": 25,
    "ties": 0,
    "net_score": 0,
    "win_rate": 0.5,
    "avg_points_per_game": 0.05
  },
  {
    "strategy_id": 7,
    "opponent_strategy_id": 9,
    "wins": 35,
    "losses": 15,
    "ties": 0,
    "net_score": 20,
    "win_rate": 0.7,
    "avg_points_per_game": 0.2
  },
  ...
]
```

#### Response fields

| Field                  | Type   | Description                                              |
| ---------------------- | ------ | -------------------------------------------------------- |
| `strategy_id`          | int    | ID of the strategy                                       |
| `opponent_strategy_id` | int    | ID of the opposing strategy in this game                 |
| `wins`                 | str    | Number of games this strategy won against that opponent  |
| `losses`               | number | Number of games this strategy lost against that opponent |
| `ties`                 | number | Number of tied games                                     |
| `net_score`            | number | Difference `wins - losses`                               |
| `win_rate`             | number | `wins / (wins + losses)`, rounded to 4 decimal places    |
| `avg_points_per_game`  | number | Average of normalized `score` per game vs this opponent  |

## 5. Error Handling

All endpoints return standard HTTP status codes and a JSON error payload. Your client code should inspect the status and react accordingly.

### 5.1 Common Error Responses

| HTTP Code | Error Key               | When It Occurs                                                             | Recommended Client Action                              |
| :-------: | :---------------------- | :------------------------------------------------------------------------- | :----------------------------------------------------- |
|  **400**  | `Bad Request`           | Request parameters are missing, invalid or out of range.                   | Check parameter names/types; correct and retry.        |
|  **401**  | `Unauthorized`          | Missing or invalid `X-API-KEY` header.                                     | Verify & supply a valid API key; prompt user to login. |
|  **404**  | `Not Found`             | Resource doesn’t exist or isn’t visible to you (e.g. arena/game/strategy). | Inform user “not found” or use fallback logic.         |
|  **429**  | `Too Many Requests`     | You’ve exceeded your rate limit.                                           | Back off (e.g. exponential retry), then retry later.   |
| **500+**  | `Internal Server Error` | Unexpected server failure.                                                 | Retry after a delay; if persistent, report to support. |

#### Error Payload Format

```json
{
  "error": "Not Found",
  "details": "Arena not found."
}
```

### 5.2 Example for error handling using RPSAClient

```python
from rpsa_client import RPSAClient
from rpsa_client.exceptions import (
    UnauthorizedError,
    NotFoundError,
    BadRequestError,
    RateLimitError,
    APIError
)

BASE_URL = "rockpapercode.onespire.hu/api/v1/public"
API_KEY = "your_api_key"

client = RPSAClient(api_key=API_KEY, base_url=BASE_URL)

try:
    arena = client.get_arena(arena_id=999)
    print("Arena details:", arena)
except UnauthorizedError:
    print("Invalid or missing API key")
except NotFoundError:
    print("Arena not found")
except BadRequestError as e:
    print("Bad request:", e)
except RateLimitError:
    print("Too many requests – slow down or back off")
except APIError as e:
    print("Server error or unexpected response:", e)
finally:
    client.close()
```

## 6 Summary

### Arenas Endpoints

| Method | Path                             | Params                                                 | Description                                                        |
| :----- | :------------------------------- | :----------------------------------------------------- | :----------------------------------------------------------------- |
| GET    | `/arenas`                        | Query: `page`, `per_page`                              | Paginated list of **regular** arenas + your irregular arenas.      |
| GET    | `/arenas/{arena_id}`             | Path: `arena_id`                                       | Metadata & aggregates for one arena (must be regular or yours).    |
| GET    | `/arenas/{arena_id}/games`       | Path: `arena_id` <br>Query: `page`, `per_page`, `sort` | Paginated games in an arena you can view.                          |
| GET    | `/arenas/{arena_id}/leaderboard` | Path: `arena_id`                                       | Per-strategy ranking (total_score, wins, losses, win_rate, …).     |
| GET    | `/arenas/{arena_id}/matchups`    | Path: `arena_id`                                       | Head-to-head aggregates (wins, net_score, avg_points_per_game, …). |

---

### Games Endpoints

| Method | Path               | Params                            | Description                              |
| :----- | :----------------- | :-------------------------------- | :--------------------------------------- |
| GET    | `/games`           | Query: `page`, `per_page`, `sort` | Paginated list of all games you may see. |
| GET    | `/games/{game_id}` | Path: `game_id`                   | All result rows for a specific game.     |

---

### Strategies Endpoints

| Method | Path                                     | Params                            | Description                                                                          |
| :----- | :--------------------------------------- | :-------------------------------- | :----------------------------------------------------------------------------------- |
| GET    | `/strategies`                            | Query: `page`, `per_page`, `sort` | Paginated list of strategies with aggregated stats (plays, total_score, win_rate).   |
| GET    | `/strategies/{strategy_id}/results`      | Path: `strategy_id`               | Aggregated performance for one strategy (wins, losses, ties, total_score, win_rate). |
| GET    | `/strategies/{strategy_id}/head_to_head` | Path: `strategy_id`               | Per-opponent head-to-head metrics (wins, net_score, avg_points_per_game, win_rate).  |
