"""
Created 05/02/2021
DynamoDB Model for a User
"""
from app.main.models.metadata import DefaultMeta
from app.main.config import Config
from argon2 import PasswordHasher
from datetime import datetime
from app.main.constants import UserRoles
from uuid import uuid4
from argon2.exceptions import VerifyMismatchError
from pynamodb.attributes import UTCDateTimeAttribute, UnicodeAttribute
from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection, LocalSecondaryIndex


class UserIndex(GlobalSecondaryIndex):
    """ User Indexes """
    class Meta(DefaultMeta):
        """ Metadata for User Index """
        projection = KeysOnlyProjection()

    user_id = UnicodeAttribute(default=lambda: str(uuid4()), hash_key=True)


class User(Model):
    """
    DynamoDB Model for a User
    user_id: str        # UUID4, Hash Key, Public ID
    village_id: str     # UUID4, the user's associated village ID
    name: str           # The user's name
    username: str       # The user's username
    password: str       # Argon2 Hash of the user's password
    role: str           # The user's role in the system
    created_on: Date    # Creation timestamp
    """
    class Meta(DefaultMeta):
        """ Metadata for User Table """
        table_name = Config.Tables.USERS
        region = Config.AWS_REGION

    user_id = UnicodeAttribute(default=lambda: str(uuid4()))
    village_id = UnicodeAttribute(null=True)
    name = UnicodeAttribute(null=False)
    username = UnicodeAttribute(hash_key=True, null=False)
    password = UnicodeAttribute(null=False)
    role = UnicodeAttribute(default=UserRoles.USER)
    created_on = UTCDateTimeAttribute(default=datetime.now)
    index = UserIndex()

    @property
    def dictionary(self) -> dict:
        """ A representation of a User as a dict """
        values = self.attribute_values.copy()
        del values["password"]
        values["created_on"] = values["created_on"].isoformat()
        return values

    def set_password(self, raw_password: str):
        """ Hash and set the password """
        self.password = PasswordHasher().hash(raw_password)

    def verify_password(self, raw_password: str):
        """ Verifies the provided password against the hashed password """
        hasher = PasswordHasher()

        try:
            hasher.verify(self.password, raw_password)

            if hasher.check_needs_rehash(self.password):
                self.set_password(self.password)
                self.save()
            return True

        except VerifyMismatchError:
            return False
