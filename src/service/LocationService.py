from sqlalchemy.orm import Session

from src.exception.CustomException import *
from src.mapper.LocationMapper import LocationMapper
from src.vo.LocationVO import LocationVO
from src.dto.LocationDTO import *

class LocationService:
    mapper = LocationMapper()

    def insert(self, vo: LocationVO):
        try:
            self.mapper.insert(vo)
        except Exception:
            raise CreateException()

    def read_all(self, db: Session):
        try:
            return self.mapper.read_all(db)
        except Exception:
            raise ReadException()

    def read_id(self, location_id: int):
        try:
            return self.mapper.read_id(location_id)
        except Exception:
            raise ReadException()

    def read_name(self, location_name: str):
        try:
            return self.mapper.read_name(location_name)
        except Exception:
            raise ReadException()

    def update(self, vo: LocationVO):
        try:
            self.mapper.update(vo)
        except Exception:
            raise UpdateException()
