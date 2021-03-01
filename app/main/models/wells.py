from .. import db

class Wells(db.model):
    __tablename__ = "Wells"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country = db.Column(db.String(100), unique=True, index=True)
    district = db.Column(db.String(100), unique=True, index=True)
    sub_district = db.Column(db.String(100), unique=True, index=True)
    village = db.Column(db.String(100), unique=True, index=True)
    latitude = db.Column(db.Float, unique=True, index=True)
    longitude = db.Column(db.Float, unique=True, index=True)

    def __repr__(self):
        return f"<Well id='{self.id}' country='{self.country}' district='{self.district}' sub district='{self.sub_district}' village='{self.village}' latitude='{self.latitude}' longitude='{self.longitude}'>"

    def to_object(self):
        return {
            "well id": self.id,
            "country": self.country,
            "district": self.district,
            "sub district": self.sub_district,
            "village": self.village,
            "latitude": self.latitude,
            "longitude": self.longitude
        }