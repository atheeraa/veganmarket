import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()


class Department(Base):
    __tablename__ = 'Department'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    image = Column(Text(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Item(Base):
    __tablename__ = 'Item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    department_id = Column(Integer, ForeignKey('Department.id'))
    department = relationship(Department)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'course': self.course,
        }


engine = create_engine('sqlite:///veganmarket.db')


Base.metadata.create_all(engine)
