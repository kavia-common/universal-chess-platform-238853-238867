from typing import Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

from app.core.security import issue_token, verify_token

router = APIRouter()
security = HTTPBearer(auto_error=False)

# In-memory store for scaffold/demo only.
_USERS: Dict[str, Dict[str, str]] = {}  # user_id -> {email, password}


class RegisterRequest(BaseModel):
    """User registration request (scaffold)."""

    email: str = Field(..., description="User email address.")
    password: str = Field(..., min_length=4, description="User password (plain text in scaffold).")


class LoginRequest(BaseModel):
    """User login request (scaffold)."""

    email: str = Field(..., description="User email address.")
    password: str = Field(..., description="User password.")


class AuthTokenResponse(BaseModel):
    """Auth token response."""

    access_token: str = Field(..., description="Bearer token for authenticated requests.")
    token_type: str = Field(default="bearer", description="Token type.")


class MeResponse(BaseModel):
    """Current user response."""

    user_id: str = Field(..., description="User identifier.")
    email: str = Field(..., description="User email address.")


def _get_user_by_email(email: str) -> Optional[Dict[str, str]]:
    for uid, data in _USERS.items():
        if data["email"].lower() == email.lower():
            return {"user_id": uid, **data}
    return None


def _require_user(creds: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> MeResponse:
    """Dependency to require a valid bearer token."""
    if not creds or not creds.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token.")
    payload = verify_token(creds.credentials)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token.")
    user_id = str(payload["sub"])
    user = _USERS.get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found.")
    return MeResponse(user_id=user_id, email=user["email"])


@router.post(
    "/register",
    summary="Register a new user (scaffold)",
    description="Creates a user in an in-memory store. Not production-ready.",
    response_model=MeResponse,
    operation_id="register_user",
)
# PUBLIC_INTERFACE
def register_user(body: RegisterRequest) -> MeResponse:
    """Register a user (scaffold)."""
    existing = _get_user_by_email(body.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered.")
    user_id = f"user_{len(_USERS) + 1}"
    _USERS[user_id] = {"email": body.email, "password": body.password}
    return MeResponse(user_id=user_id, email=body.email)


@router.post(
    "/login",
    summary="Login (scaffold)",
    description="Validates user credentials against an in-memory store and returns a signed token.",
    response_model=AuthTokenResponse,
    operation_id="login_user",
)
# PUBLIC_INTERFACE
def login_user(body: LoginRequest) -> AuthTokenResponse:
    """Login a user (scaffold)."""
    user = _get_user_by_email(body.email)
    if not user or user["password"] != body.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")
    token = issue_token(subject=user["user_id"])
    return AuthTokenResponse(access_token=token)


@router.get(
    "/me",
    summary="Get current user (scaffold)",
    description="Returns the authenticated user based on the bearer token.",
    response_model=MeResponse,
    operation_id="get_current_user",
)
# PUBLIC_INTERFACE
def get_me(me: MeResponse = Depends(_require_user)) -> MeResponse:
    """Get authenticated user profile (scaffold)."""
    return me
