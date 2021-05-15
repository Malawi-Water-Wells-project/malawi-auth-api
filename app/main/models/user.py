"""
Created 05/02/2021
SQLAlchemy Model for a User
"""
from app.main.models import db
from argon2 import PasswordHasher


class User(db.Model):
    """
    SQLAlchemy model for a User
    id: int             # Primary Key, autoincrement
    tribe_id: str       # The user's associated tribe ID
    public_id: str      # The user's "Public ID" to be used in requests
    username: str       # The user's username
    password_hash: str  # Argon2 Hash of the user's password
    name: str           # The user's name
    role: str           # The user's role in the system
    created_on: Date    # Creation timestamp
    """

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
        return "<User " + \
            f"id='{self.id}' " +\
            f"name='{self.name}' " + \
            f"tribe_id='{self.tribe_id}' " + \
            f"role='{self.role}' " + \
            f"created_on='{self.created_on}'>"

    @property
    def password(self):
        """ This is just for the setter! Don't use me! """
        raise AttributeError("Don't access the password directly!")

    @password.setter
    def password(self, password: str):
        """
        Setter for self.password_hash, hashes and salts the password using Argon2
        """
        password_hasher = PasswordHasher()
        self.password_hash = password_hasher.hash(password)

    def verify_password(self, password: str) -> bool:
        """
        Verifies the raw password against the stored hash.
        Returns a boolean value is_valid
        """
        password_hasher = PasswordHasher()
        is_valid = password_hasher.verify(self.password_hash, password)

        # TODO: Password revalidation
        return is_valid

    @property
    def dictionary(self):
        """ A representation of the user as a dictionary """
        return {
            "id": self.id,
            "tribe_id": self.tribe_id,
            "public_id": self.public_id,
            "name": self.name,
            "role": self.role,
            "username": self.username,
            "created_on": self.created_on.isoformat()  # pylint: disable=no-member
        }
