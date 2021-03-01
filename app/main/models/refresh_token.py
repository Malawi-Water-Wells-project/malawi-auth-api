from . import db


class RefreshToken(db.Model):
    __tablename__ = "Refresh_Tokens"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String, unique=True, index=True)
    user_id = db.Column(db.Integer, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    revoked = db.Column(db.Boolean)

    def __repr__(self):
        return f"<RefreshToken token='{self.token}' user_id='{self.user_id}' expires_at='{self.expires_at}'"
