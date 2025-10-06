from sqlalchemy import Column, Integer, String
from db import Base  

class Place(Base):
    __tablename__ = "places"  

    id = Column(Integer, primary_key=True, index=True)  
    name = Column(String(200))
    address = Column(String(300))
    city = Column(String(100))
    country = Column(String(100))

    def __repr__(self):
        return f"<Place {self.id} {self.name}>"



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)

    def __repr__(self):
        return f"<User {self.id} {self.username}>"