from app.main.service.token_service import store_refresh_token
import jwt
from ..config import secret_key
from datetime import datetime, timedelta


def generate_jwt_keypair(user_id, tribe_id, role):
    base_claims = {
        "user_id": user_id,
        "tribe_id": tribe_id,
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

    refresh_token_expiry = datetime.utcnow() + timedelta(weeks=52)
    refresh_token = jwt.encode(
        {
            **base_claims,
            "exp": refresh_token_expiry
        },
        secret_key,
        algorithm="HS256"
    )

    store_refresh_token(refresh_token, refresh_token_expiry, user_id)

    return access_token, refresh_token


def validate_access_token(token: str):
    if "Bearer" in token:
        token = token.split("Bearer").pop().strip()

    try:
        payload = jwt.decode(token, secret_key, algorithm="HS256")
        return None, payload

    except jwt.ExpiredSignatureError:
        return "Access Token Expired", None

    except jwt.InvalidTokenError:
        return "Invalid Access Token", None


def validate_refresh_token(token):
    pass
