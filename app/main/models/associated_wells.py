from .. import db

class AssociatedWells(db.Model):
    __tablename__ = "associated_wells"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tribe_id = db.Column(db.Integer, db.ForeignKey('Tribe.id')
    
    


    def __repr__(self):
        return f"AssociatedWells id='{self.id}'"

    def to_object(self):
        return {
            "id": self.id,
        }