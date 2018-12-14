from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()



class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

class Department(Base):
    __tablename__ = 'Department'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    image = Column(Text(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
             'id': self.id,
            'name': self.name,
            'image': self.image,
        }


class Item(Base):
    __tablename__ = 'Item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    department_id = Column(Integer, ForeignKey('Department.id'))
    department = relationship(Department)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price':self.price,
        }


engine = create_engine('sqlite:///veganmarket.db')


Base.metadata.create_all(engine)
