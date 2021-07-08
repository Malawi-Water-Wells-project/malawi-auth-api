"""
Created 17/06/2021
DynamoDB Join Token Model
"""
from datetime import datetime, timedelta
from pynamodb.models import Model
from pynamodb.attributes import TTLAttribute, UnicodeAttribute
from uuid import uuid4


def defaultTokenTimeToLive():
    """ Returns the default TTL for the Join Token (15 mins) """
    return datetime.now() + timedelta(minutes=15)


class JoinToken(Model):
    """
    DynamoDB Model for a Join Token
    """
    token_id = UnicodeAttribute(default=lambda: str(uuid4()), hash_key=True)
    tribe_id = UnicodeAttribute()
    tribe_name = UnicodeAttribute()
    ttl = TTLAttribute(default=defaultTokenTimeToLive)

    @property
    def dictionary(self):
        """ A representation of the Join Token as a dictionary """
        values = self.attribute_values.copy()
        values["ttl"] = values["ttl"].timestamp()
        return values
