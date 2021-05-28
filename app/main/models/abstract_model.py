"""
Created 25/05/2021
Abstract Model Class
"""
from app.main.models import db

class AbstractModel:
    def save(self):
        """ Save the model """
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """ Delete the model """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def create(cls, **kwargs):
        """ Create an instance of the class """
        instance = cls(**kwargs)
        instance.save()
        return instance

    def _is_new_record(self) -> bool:
        return self.id is not None

    @property
    def dictionary(self) -> dict:
        raise NotImplementedError("Implement Me!")
