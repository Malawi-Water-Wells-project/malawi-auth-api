from .. import db


class Well(db.Model):
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
        return f"<Well id='{self.id}' well_id='{self.well_id}' country='{self.country}' district='{self.district}' sub_district='{self.sub_district}' village='{self.village}' latitude='{self.latitude}' longitude='{self.longitude}'>"

    def to_object(self):
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
