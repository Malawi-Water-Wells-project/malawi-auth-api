from .. import db
from argon2 import PasswordHasher


class User(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tribe_id = db.Column(db.Integer, db.ForeignKey('Tribe.id'))
    public_id = db.Column(db.String(100), unique=True, index=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<User id='{self.id}' name='{self.name}' tribe_id='{self.tribe_id}' role='{self.role}' created_on='{self.created_on}'>"

    @property
    def password(self):
        raise AttributeError("Don't access the password directly!")

    @password.setter
    def password(self, password: str):
        ph = PasswordHasher()
        self.password_hash = ph.hash(password)

    def verify_password(self, password: str):
        ph = PasswordHasher()
        is_valid = ph.verify(self.password_hash, password)

        # TODO: Password revalidation

        if is_valid is False:
            return False

        return True

    def to_object(self):
        return {
            "id": self.id,
            "tribe_id": self.tribe_id,
            "public_id": self.public_id,
            "name": self.name,
            "role": self.role,
            "username": self.username,
            "created_on": self.created_on.isoformat()
        }
