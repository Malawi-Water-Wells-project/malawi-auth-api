"""
Created: 08/02/2021
SQLAlchemy Model for a Refresh Token
"""
from app.main.config import Config
from datetime import datetime
from pynamodb.attributes import BooleanAttribute, UTCDateTimeAttribute, UnicodeAttribute
from pynamodb.models import Model
from pynamodb.indexes import KeysOnlyProjection, GlobalSecondaryIndex


class RefreshTokenUserIndex(GlobalSecondaryIndex):
    """ Global Index for querying refresh tokens by User ID """
    class Meta:
        """ Refresh Token Index Metadata """
        projection = KeysOnlyProjection()
        region = Config.AWS_REGION

    user_id = UnicodeAttribute(null=False, hash_key=True)


class RefreshToken(Model):
    """
    DynamoDB Model for a Refresh Token
    token: str              # The encoded JWT
    user_id: str            # The associated user ID
    expires_at: datetime    # Expiry date of the token
    revoked: bool           # Revoked status of the token (True=revoked, False=valid)
    """
    class Meta:
        """ Metadata for RefreshToken Table """
        table_name = Config.Tables.REFRESH_TOKENS
        region = Config.AWS_REGION

    token: str = UnicodeAttribute(hash_key=True, null=False)
    user_id: str = UnicodeAttribute(null=False)
    expires_at: datetime = UTCDateTimeAttribute(null=False)
    revoked: bool = BooleanAttribute(null=False, default=False)
    user_index = RefreshTokenUserIndex()

    def __repr__(self):
        return "<RefreshToken " + \
            f"token='{self.token}' " + \
            f"user_id='{self.user_id}' " + \
            f"expires_at='{self.expires_at}' " + \
            f"revoked={self.revoked}>"
