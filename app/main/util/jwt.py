"""
Created 08/02/2021
JWT Creation Utils
"""

from datetime import datetime, timedelta
from typing import Tuple, Union

from app.main.config import secret_key
import jwt


def generate_access_token(user_id: int, village_id: str, role: str) -> str:
    """ Generate an access token that expires in 15 minutes """
    base_claims = {
        "user_id": user_id,
        "village_id": village_id,
        "role": role,
        "iat": datetime.utcnow()
    }

    access_token = jwt.encode(
        {
            **base_claims,
            "exp": datetime.utcnow() + timedelta(minutes=15)
        },
        secret_key,
        algorithm="HS256"
    )

    return access_token




def validate_access_token(token: str) -> Union[Tuple[None, dict], Tuple[str, None]]:
    """ Validates an access token """
    if "Bearer" in token:
        token = token.split("Bearer").pop().strip()

    try:
        payload = jwt.decode(token, secret_key, algorithms="HS256")
        return None, payload

    except jwt.ExpiredSignatureError:
        return "Access Token Expired", None

    except jwt.InvalidTokenError:
        return "Invalid Access Token", None


def validate_refresh_token(token: str) -> Union[Tuple[None, dict], Tuple[str, None]]:
    """ Validates a refresh token """
    if "Bearer" in token:
        token = token.split("Bearer").pop().strip()

    try:
        payload = jwt.decode(token, secret_key, algorithms="HS256")
        return None, payload

    except jwt.ExpiredSignatureError:
        return "Refresh Token Expired", None

    except jwt.InvalidTokenError:
        return "Invalid Refresh Token", None
