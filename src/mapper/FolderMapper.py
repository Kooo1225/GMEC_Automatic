from sqlalchemy.orm import Session
from src.vo.FolderVO import FolderVO


class FolderMapper:
    def insert(self, vo: FolderVO, db: Session):
        new_record = vo
        db.add(new_record)
        db.commit()

    def read_all(self, db: Session):
        return db.query(FolderVO).all()

    def read_id(self, folder_id: int, db: Session):
        return db.query(FolderVO).filter(FolderVO.folder_id == folder_id).first()

    def read_location(self, location_id: int, db: Session):
        return db.query(FolderVO).filter(FolderVO.location_id == location_id).all()

    def update(self, vo: FolderVO, db: Session):
        record = db.query(FolderVO).filter(FolderVO.folder_id == vo.folder_id).first()
        record.folder_name = vo.folder_name
        record.location_id = vo.location_id
        record.due_date = vo.due_date
        record.marks = vo.marks
        db.commit()

    def delete(self, folder_id: int, db: Session):
        record = db.query(FolderVO).filter(FolderVO.folder_id == folder_id).first()
        db.delete(record)
        db.commit()
