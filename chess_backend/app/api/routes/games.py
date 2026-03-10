from __future__ import annotations

from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter()

# In-memory game store for scaffold/demo only.
_GAMES: Dict[str, "GameState"] = {}


class CreateGameRequest(BaseModel):
    """Create game request (scaffold)."""

    white_user_id: str = Field(..., description="User id playing white.")
    black_user_id: str = Field(..., description="User id playing black.")
    initial_fen: str = Field(
        default="startpos",
        description="Initial position in FEN, or 'startpos' for standard start. Validation not implemented yet.",
    )


class MoveSubmitRequest(BaseModel):
    """Move submission request (scaffold)."""

    by_user_id: str = Field(..., description="User id making the move.")
    move_uci: str = Field(..., description="Move in UCI format (e.g. e2e4). Validation not implemented yet.")


class GameState(BaseModel):
    """Game state (scaffold).

    NOTE: This does not implement full chess rules. It is a minimal placeholder to support API shape.
    """

    game_id: str = Field(..., description="Game identifier.")
    white_user_id: str = Field(..., description="White player user id.")
    black_user_id: str = Field(..., description="Black player user id.")
    initial_fen: str = Field(..., description="Initial FEN or 'startpos'.")
    moves_uci: List[str] = Field(default_factory=list, description="Moves in UCI format, in order.")
    status: str = Field(default="active", description="Game status: active|finished|aborted.")
    winner_user_id: Optional[str] = Field(default=None, description="Winner user id if finished.")


class GameCreatedResponse(BaseModel):
    """Create game response."""

    game: GameState = Field(..., description="Created game state.")


class GameListResponse(BaseModel):
    """List games response."""

    games: List[GameState] = Field(..., description="All games currently in memory.")


@router.post(
    "",
    summary="Create a game (scaffold)",
    description="Creates a new in-memory game record with two players.",
    response_model=GameCreatedResponse,
    operation_id="create_game",
)
# PUBLIC_INTERFACE
def create_game(body: CreateGameRequest) -> GameCreatedResponse:
    """Create a new game (scaffold)."""
    game_id = f"game_{len(_GAMES) + 1}"
    game = GameState(
        game_id=game_id,
        white_user_id=body.white_user_id,
        black_user_id=body.black_user_id,
        initial_fen=body.initial_fen,
    )
    _GAMES[game_id] = game
    return GameCreatedResponse(game=game)


@router.get(
    "",
    summary="List games (scaffold)",
    description="Lists all in-memory games.",
    response_model=GameListResponse,
    operation_id="list_games",
)
# PUBLIC_INTERFACE
def list_games() -> GameListResponse:
    """List games (scaffold)."""
    return GameListResponse(games=list(_GAMES.values()))


@router.get(
    "/{game_id}",
    summary="Get game state (scaffold)",
    description="Returns the current in-memory state for a given game.",
    response_model=GameState,
    operation_id="get_game",
)
# PUBLIC_INTERFACE
def get_game(game_id: str) -> GameState:
    """Get a game by id (scaffold)."""
    game = _GAMES.get(game_id)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found.")
    return game


@router.post(
    "/{game_id}/moves",
    summary="Submit a move (scaffold)",
    description="Appends a move to the game's move list. Does not validate legality in this scaffold.",
    response_model=GameState,
    operation_id="submit_move",
)
# PUBLIC_INTERFACE
def submit_move(game_id: str, body: MoveSubmitRequest) -> GameState:
    """Submit a move to the given game (scaffold)."""
    game = _GAMES.get(game_id)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found.")
    if body.by_user_id not in (game.white_user_id, game.black_user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a player in this game.")
    if not body.move_uci or len(body.move_uci) < 4:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid move format.")
    game.moves_uci.append(body.move_uci)
    _GAMES[game_id] = game
    return game
