"""
Created 05/02/2021
SQLAlchemy Model for a Tribe
"""
from app.main.models import db


class Tribe(db.Model):
    """
    SQLAlchemy Model for a Tribe
    id: int             # Primary Key, autoincrement
    public_id: str      # Tribe's "Public ID" to be used in requests
    name: str           # Tribe's name
    latitude: float     # Tribe's latitude
    longitude: float    # Tribe's longitude
    created_on: Date    # Creation timestamp
    users: Relationship(User) # One-to-Many Relationship with Users
    """
    __tablename__ = "Tribe"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), unique=True, index=True)
    name = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    users = db.relationship("User")

    def __repr__(self):
        return "<Tribe " + \
            f"id='{self.id}' " + \
            f"public_id='{self.public_id}' " + \
            f"name='{self.name}' " + \
            f"latitude='{self.latitude}' " + \
            f"longitude='{self.longitude}'>"

    @property
    def dictionary(self):
        """ A representation of the user as a dictionary """
        return {
            "id": self.id,
            "public_id": self.public_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "name": self.name,
            "created_on": self.created_on.isoformat()  # pylint: disable=no-member
        }
