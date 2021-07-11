"""
Created 08/02/2021
DB Access Service for Tokens
"""

from app.main.models.refresh_token import RefreshToken
from datetime import datetime, timedelta
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
        claims = {
            "user_id": user_id,
            "tribe_id": tribe_id,
            "role": role,
            "iat": datetime.now()
        }
        access_token = cls.create_access_token(**claims)
        refresh_token = cls.create_refresh_token(**claims)

        return access_token, refresh_token

    @classmethod
    def create_access_token(cls, **kwargs):
        """ Creates an access token JWT """
        issue_time = kwargs.get("iat", datetime.now())
        return cls._encode_jwt(
            user_id=kwargs.get("user_id"),
            tribe_id=kwargs.get("tribe_id"),
            role=kwargs.get("role"),
            iat=issue_time,
            exp=issue_time + timedelta(seconds=cls.ACCESS_TOKEN_LIFESPAN)
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
        expiry_time = issue_time + \
            timedelta(seconds=cls.REFRESH_TOKEN_LIFESPAN)
        encoded_jwt = cls._encode_jwt(
            user_id=user_id,
            tribe_id=tribe_id,
            role=role,
            iat=issue_time,
            exp=expiry_time)
        # Create a RefreshToken DB object
        token = RefreshToken(
            token=encoded_jwt,
            user_id=user_id,
            expires_at=expiry_time,
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



    @classmethod
    def decode_refresh_token(cls, token: str):
        """ Validates a Refresh Token """
        try:
            # TODO: Check for expiry here to save an extra DB trip
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
            return decoded_token, None
        # TODO: Do some better error handling here!
        except Exception as exc:
            return None, str(exc)

    @classmethod
    def get_refresh_token_record(cls, token: str) -> Union[RefreshToken, None]:
        """ Gets the Refresh Token record """
        if "Bearer" in token:
            token = token.split(" ")[-1]

        try:
            result = RefreshToken.get(token)
            # TODO: This is a horrible hack. Fix this!
            if float(result.expires_at.timestamp()) < float(datetime.now().timestamp()):
                return None
            return result
        except RefreshToken.DoesNotExist:
            return None
