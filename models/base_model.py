#!/usr/bin/python3
"""
    A base model for all the objects
"""
from uuid import uuid4
from datetime import datetime
#from models import storage

class BaseModel:
    """
        A base model for all the objects
    """
    def __init__(self, *args, **kwargs):
        from models import storage
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """
            returns the string representation of the object
            class name + id + dict(attribures list)
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """updates the updated at attribute with the current datetime"""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()
    
    def to_dict(self):
        """
            returns all the attributes in the class obj
        """
        d = self.__dict__.copy()
        d['__class__'] = self.__class__.__name__
        d['created_at'] = self.created_at.isoformat()
        d['updated_at'] = self.updated_at.isoformat()
        return d

    