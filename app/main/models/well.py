"""
Created 01/03/2021
SQLAlchemy Model for a Well
"""
from app.main.models import db


class Well(db.Model):
    """
    SQLAlchemy Model for a Well
    id: int             # Primary Key, autoincrement
    well_id: str        # Well's ID, i.e. AAA01
    country: str        # Well's Country
    district: str       # Well's District
    sub_district: str   # Well's Sub-District
    village: str        # Well's Village
    latitude: float     # Latitude of the well
    longitude: float    # Longitude of the well
    """

    __tablename__ = "Wells"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    well_id = db.Column(db.String(10), unique=True, index=True, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    sub_district = db.Column(db.String(100), nullable=False)
    village = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return "<Well " + \
            f"id='{self.id}' " + \
            f"well_id='{self.well_id}' " + \
            f"country='{self.country}' " + \
            f"district='{self.district}' " + \
            f"sub_district='{self.sub_district}' " + \
            f"village='{self.village}' " + \
            f"latitude='{self.latitude}' " + \
            f"longitude='{self.longitude}'>"

    @property
    def dictionary(self):
        """ A representation of the well as a dictionary """
        return {
            "id": self.id,
            "well_id": self.well_id,
            "country": self.country,
            "district": self.district,
            "sub_district": self.sub_district,
            "village": self.village,
            "latitude": self.latitude,
            "longitude": self.longitude
        }
