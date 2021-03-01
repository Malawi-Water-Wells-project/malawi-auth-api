from typing import Union
from app.main.models.refresh_token import RefreshToken
from app.main.models import db


def store_refresh_token(token, expiry, user_id):
    refresh_token = RefreshToken(
        token=token,
        expires_at=expiry,
        user_id=user_id,
        revoked=False
    )

    db.session.add(refresh_token)
    db.session.commit()


def get_refresh_token(token) -> Union[RefreshToken, None]:
    return RefreshToken.query.filter_by(token=token).first()
