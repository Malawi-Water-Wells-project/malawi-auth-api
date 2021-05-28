"""
Created: 08/02/2021
SQLAlchemy Model for a Refresh Token
"""
from app.main.models.abstract_model import AbstractModel
from app.main.models import db


class RefreshToken(db.Model, AbstractModel):
    """
    SQLAlchemy Model for a Refresh Token
    id: int             # Primary Key, autoincrement
    token: str          # The encoded JWT
    user_id: int        # The associated user ID
    expires_at: Date    # Expiry date of the token
    revoked: bool       # Revoked status of the token (True=revoked, False=valid)
    """
    __tablename__ = "Refresh_Tokens"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String, unique=True, index=True)
    user_id = db.Column(db.Integer, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    revoked = db.Column(db.Boolean)

    def __repr__(self):
        return "<RefreshToken " + \
            f"token='{self.token}' " + \
            f"user_id='{self.user_id}' " + \
            f"expires_at='{self.expires_at}'>"
