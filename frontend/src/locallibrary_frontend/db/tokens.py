from sqlalchemy.orm import Session as OrmSession

from locallibrary_frontend.db.models import RefreshToken, User


def create_refresh_token(session: OrmSession, *, user: User, token: str, provider: str):
    """Create a refresh token for user."""
    refresh_token = RefreshToken(refresh_token=token, provider=provider)
    refresh_token.user = user
    session.add(refresh_token)
