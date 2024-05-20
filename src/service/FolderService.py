from sqlalchemy.orm import Session

from src.exception.CustomException import *
from src.mapper.FolderMapper import FolderMapper
from src.vo.FolderVO import FolderVO
from src.dto.FolderDTO import *


class FolderService:
    mapper = FolderMapper()

    def insert(self, dto: InsertFolderDTO, db: Session):
        try:
            self.mapper.insert(dto, db)
        except Exception:
            raise CreateException()

    def read_all(self, db: Session):
        try:
            return self.mapper.read_all(db)
        except Exception:
            raise ReadException()

    def read_id(self, folder_id, db: Session):
        try:
            return self.mapper.read_id(folder_id, db)
        except Exception:
            raise ReadException()

    def read_location(self, location_id, db: Session):
        try:
            return self.mapper.read_location(location_id, db)
        except Exception:
            raise ReadException()

    def update(self, dto: FolderDTOinDB, db: Session):
        try:
            self.mapper.update(dto, db)
        except Exception:
            raise UpdateException()

    def delete(self, folder_id: int, db: Session):
        try:
            self.mapper.delete(folder_id, db)
        except Exception:
            raise DeleteException()