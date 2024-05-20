from sqlalchemy.orm import Session
from src.vo.LocationVO import LocationVO

class LocationMapper:
    def insert(self, vo: LocationVO, db: Session):
        new_record = vo
        db.add(new_record)
        db.commit()

    def read_all(self, db: Session):
        return db.query(LocationVO).all()

    def read_id(self, location_id: int, db: Session):
        return db.query(LocationVO).filter(LocationVO.location_id == location_id).first()

    def read_name(self, location_name: str, db: Session):
        return db.query(LocationVO).filter(LocationVO.location_name == location_name).all()

    def update(self, vo: LocationVO, db: Session):
        record = db.query(LocationVO).filter(LocationVO.location_id == vo.location_id).first()
        record.location_name = vo.location_name
        db.commit()

    def delete(self, location_id: int, db: Session):
        record = db.query(LocationVO).filter(LocationVO.location_id == location_id).first()
        db.delete(record)
        db.commit()
