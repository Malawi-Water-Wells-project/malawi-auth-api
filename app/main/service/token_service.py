"""
Created 08/02/2021
DB Access Service for Tokens
"""

from typing import Union

from app.main.models import db
from app.main.models.refresh_token import RefreshToken


def store_refresh_token(token, expiry, user_id) -> RefreshToken:
    """ Stores a new RefreshToken in the DB """
    refresh_token = RefreshToken(
        token=token,
        expires_at=expiry,
        user_id=user_id,
        revoked=False
    )

    db.session.add(refresh_token)
    db.session.commit()
    return refresh_token


def get_refresh_token(token) -> Union[RefreshToken, None]:
    """ Retrieves a RefreshToken by JWT """
    return RefreshToken.query.filter_by(token=token).first()
