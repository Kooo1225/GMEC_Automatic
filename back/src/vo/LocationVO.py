from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

BASE = declarative_base()

class LocationVO(BASE):
    __tablename__ = 'Location'
    location_id = Column(Integer, primary_key=True)
    location_name = Column(String)

    def __init__(self, location_name, location_id=None):
        self.location_id = location_id
        self.location_name = location_name

    def __repr__(self):
        return f"LocationVO(location_id={self.location_id}, location_name={self.location_name})"
