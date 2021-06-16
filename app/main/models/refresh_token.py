"""
Created: 08/02/2021
SQLAlchemy Model for a Refresh Token
"""
from datetime import datetime
from uuid import uuid4
from pynamodb.attributes import BooleanAttribute, UTCDateTimeAttribute, UnicodeAttribute
from pynamodb.models import Model


class RefreshToken(Model):
    """
    DynamoDB Model for a Refresh Token
    token_id: str                 # UUID4, Hash Key
    token: str              # The encoded JWT
    user_id: str            # The associated user ID
    expires_at: datetime    # Expiry date of the token
    revoked: bool           # Revoked status of the token (True=revoked, False=valid)
    """
    class Meta:
        """ Metadata for RefreshToken Table """
        table_name = "dynamodb-refreshtoken"
        host = "http://localhost:8000"
        read_capacity_units = 1
        write_capacity_units = 1

    token_id: str = UnicodeAttribute(hash_key=True, default=uuid4)
    token: str = UnicodeAttribute(null=False)
    user_id: str = UnicodeAttribute(null=False)
    expires_at: datetime = UTCDateTimeAttribute(null=False)
    revoked: bool = BooleanAttribute(null=False)

    def __repr__(self):
        return "<RefreshToken " + \
            f"token_id='{self.token_id}' " + \
            f"token='{self.token}' " + \
            f"user_id='{self.user_id}' " + \
            f"expires_at='{self.expires_at}' " + \
            f"revoked={self.revoked}>"
