"""
Created 20/05/2021
SQLAlchemy Model for Well Hygiene
"""
from app.main.models import db


class WellHygiene(db.Model):
    __tablename__ = "well_hygiene"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tc_dry = db.Column(db.String, nullable=True, index=True)
    tc_wet = db.Column(db.Float, nullable=True, index=True)
    fc_dry = db.Column(db.Float, nullable=True, index=True)
    fc_wet = db.Column(db.Float, nullable=True, index=True)
    turbidity_dry = db.Column(db.Float, nullable=True, index=True)
    turbidity_wet = db.Column(db.Float, nullable=True, index=True)
    tds_dry = db.Column(db.Float, nullable=True, index=True)
    tds_wet = db.Column(db.Float, nullable=True, index=True)
    electrical_conductivity_dry = db.Column(
        db.Float, nullable=True, index=True)
    electrical_conductivity_wet = db.Column(
        db.Float, nullable=True, index=True)
    ph_dry = db.Column(db.Float, nullable=True, index=True)
    ph_wet = db.Column(db.Float, nullable=True, index=True)
    temperature_dry = db.Column(db.Float, nullable=True, index=True)
    temperature_wet = db.Column(db.Float, nullable=True, index=True)
    fluoride_dry = db.Column(db.Float, nullable=True, index=True)
    fluoride_wet = db.Column(db.Float, nullable=True, index=True)
    sulphate_dry = db.Column(db.Float, nullable=True, index=True)
    sulphate_wet = db.Column(db.Float, nullable=True, index=True)
    hardness_dry = db.Column(db.Float, nullable=True, index=True)
    hardness_wet = db.Column(db.Float, nullable=True, index=True)
    nitrate_dry = db.Column(db.Float, nullable=True, index=True)
    nitrate_wet = db.Column(db.Float, nullable=True, index=True)
    ammonia_dry = db.Column(db.Float, nullable=True, index=True)
    ammonia_wet = db.Column(db.Float, nullable=True, index=True)
    arsonic_dry = db.Column(db.Float, nullable=True, index=True)
    arsonic_wet = db.Column(db.Float, nullable=True, index=True)
    nitrate_no2_dry = db.Column(db.Float, nullable=True, index=True)
    nitrate_no2_wet = db.Column(db.Float, nullable=True, index=True)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"WellHygiene id='{self.id}' village='{self.village}' tc_dry='{self.tc_dry}' tc_wet='{self.tc_wet}' turbidity_dry='{self.turbidity_dry}' turbidity_wet='{self.turbidity_wet}' tds_dry='{self.tds_dry}' tds_wet='{self.tds_wet}' electrical_conductivity_dry='{self.electrical_conductivity_dry}' electrical_conductivity_wet='{self.electrical_conductivity_wet}' ph_dry='{self.ph_dry}' ph_wet='{self.ph_wet}' temperature_dry='{self.temperature_dry}' temperature_wet='{self.temperature_wet}' fluoride_dry='{self.fluoride_dry}' fluoride_wet='{self.fluoride_wet}' sulphate_dry='{self.sulphate_dry}' sulphate_wet='{self.sulphate_wet}' hardness_dry='{self.hardness_dry}' hardness_wet='{self.hardness_wet}' nitrate_dry='{self.nitrate_dry}' nitrate_wet='{self.nitrate_wet}' ammonia_dry='{self.ammonia_dry}' ammonia_wet='{self.ammonia_wet}' arsonic_dry='{self.arsonic_dry} arsonic_wet='{self.arsonic_wet}' nitrateno2_dry='{self.nitrateno2_dry}' nitrate_no2_wet='{self.nitrate_no2_wet}'timestamp='{self.timestamp}'"

    @property
    def dictionary(self) -> dict:
        """ A representation of the well hygiene as a dictionary """
        return {
            "id": self.id,
            "tc_dry": self.tc_dry,
            "tc_wet": self.tc_wet,
            "turbidity_dry": self.turbidity_dry,
            "turbidity_wet": self.turbidity_wet,
            "tds_dry": self.tds_dry,
            "tds_wet": self.tds_wet,
            "electrical_conductivity_dry": self.electrical_conductivity_dry,
            "electrical_conductivity_wet": self.electrical_conductivity_wet,
            "ph_dry": self.ph_dry,
            "ph_wet": self.ph_wet,
            "temperature_dry": self.temperature_dry,
            "temperature_wet": self.temperature_wet,
            "fluoride_dry": self.fluoride_dry,
            "fluoride_wet": self.fluoride_wet,
            "sulphate_dry": self.sulphate_dry,
            "sulphate_wet": self.sulphate_wet,
            "hardness_dry": self.hardness_dry,
            "hardness_wet": self.hardness_wet,
            "nitrate_dry": self.nitrate_dry,
            "nitrate_wet": self.nitrate_wet,
            "ammonia_dry": self.ammonia_dry,
            "ammonia_wet": self.ammonia_wet,
            "arsonic_dry": self.arsonic_dry,
            "arsonic_wet": self.arsonic_wet,
            "arsonic_wet": self.arsonic_wet,
            "arsonic_dry": self.arsonic_dry,
            "nitrateno2_dry": self.nitrate_no2_dry,
            "nitrate_no2_wet": self.nitrate_no2_wet,
            "timestamp": self.timestamp,
        }
