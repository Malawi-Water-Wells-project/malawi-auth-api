"""
Created 08/02/2021
DB Access Service for Tokens
"""

from app.main.models.refresh_token import RefreshToken
from datetime import datetime
from app.main.constants import UserRoles
from app.main.config import secret_key
from typing import ClassVar, Union
import jwt
from pynamodb.exceptions import DeleteError


class TokenService:
    """
    Service for handling access and refresh tokens
    Access Token Lifespan - 900 seconds (15 minutes)
    Refresh Token Lifespan - 31449600 seconds (52 weeks)
    """
    ACCESS_TOKEN_LIFESPAN = 900
    REFRESH_TOKEN_LIFESPAN = 31449600

    @classmethod
    def create_keypair(cls, user_id: str, tribe_id: Union[str, None], role: ClassVar[UserRoles]):
        """ Creates a JWT keypair (access+refresh) """
        issue_time = datetime.now()

        return cls.create_access_token(
            user_id=user_id,
            tribe_id=tribe_id,
            role=role,
            iat=issue_time
        ), cls.create_refresh_token(
            user_id=user_id,
            tribe_id=tribe_id,
            role=role,
            iat=issue_time
        ),

    @classmethod
    def create_access_token(cls, **kwargs):
        """ Creates an access token JWT """
        issue_time = kwargs.get("iat", datetime.now())
        return cls._encode_jwt(
            user_id=kwargs.get("user_id"),
            tribe_id=kwargs.get("tribe_id"),
            role=kwargs.get("role"),
            iat=issue_time,
            exp=issue_time + cls.ACCESS_TOKEN_LIFESPAN
        )

    @classmethod
    def create_refresh_token(
        cls,
        user_id: str,
        tribe_id: Union[str, None],
        role: ClassVar[UserRoles],
        iat: Union[int, None] = None
    ) -> str:
        """ Creates a refresh token JWT """
        issue_time = iat or datetime.now()
        encoded_jwt = cls._encode_jwt(
            user_id=user_id,
            tribe_id=tribe_id,
            role=role,
            iat=issue_time,
            exp=issue_time + cls.ACCESS_TOKEN_LIFESPAN
        )
        # Create a RefreshToken DB object
        token = RefreshToken(
            token=encoded_jwt,
            user_id=user_id,
            expires_at=issue_time + cls.ACCESS_TOKEN_LIFESPAN,
            revoked=False
        )
        token.save()

        return encoded_jwt

    @staticmethod
    def _encode_jwt(**claims):
        """ Encodes a JWT """
        return jwt.encode(claims, secret_key, algorithm="HS256")

    @classmethod
    def remove_tokens_for_user(cls, user_id: str):
        """ Removes all Refresh Tokens for the specified user ID """
        results = RefreshToken.user_index.query(user_id)
        for result in results:
            try:
                result.delete()
            except DeleteError:
                # TODO: Gracefully crash out here
                pass
