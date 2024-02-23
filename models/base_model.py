#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



class BaseModel:
    """A base class for all hbnb models"""

    # Define SQLAlchemy columns for id, created_at, and updated_at
    id = Column(String(60), nullable=False, primary_key=True, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instantiation of BaseModel object"""

        # Set id attribute to a new UUID if not provided
        self.id = kwargs.get('id', str(uuid4()))

        # Set created_at attribute to current datetime if not provided
        self.created_at = kwargs.get('created_at', datetime.now())

        # Set updated_at attribute to current datetime or provided value
        self.updated_at = kwargs.get('updated_at', self.created_at)

        # Set additional attributes from kwargs dynamically
        for key, value in kwargs.items():
            if key not in ["id", "created_at", "updated_at", "__class__"]:
                setattr(self, key, value)

    def __str__(self):
        """String representation of BaseModel object"""
        return '[{}] ({}) {}'.format(
            type(self).__name__, self.id, self.__dict__
        )

    def delete(self):
        """Delete current instance from FileStorage"""
        from models import storage
        storage.delete(self)

    def save(self):
        """Update updated_at with current datetime and save to storage"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Return dictionary representation of BaseModel instance"""

        # Copy instance dictionary to avoid modifying original object
        instance_dict = self.__dict__.copy()

        # Add __class__ key with class name to dictionary
        instance_dict.update({
            '__class__': type(self).__name__,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        })

        # Remove SQLAlchemy instance state key if present
        instance_dict.pop('_sa_instance_state', None)

        return instance_dict
