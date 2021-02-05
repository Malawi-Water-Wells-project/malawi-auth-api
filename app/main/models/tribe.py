from .. import db


class Tribe(db.Model):
    __tablename__ = "Tribe"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, index=True)
    name = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    users = db.relationship("User")

    def __repr__(self):
        return f"<Tribe id='{self.id}' name='{self.name}' latitude='{self.latitude}' longitude='{self.longitude}'>"

    def to_object(self):
        return {
            "id": self.id,
            "public_id": self.public_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "name": self.name,
            "created_on": self.created_on.isoformat()
        }
