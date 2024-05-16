from src.exception.CustomException import *
from src.mapper.FolderMapper import FolderMapper
from src.vo.FolderVO import FolderVO


class FolderService:
    mapper = FolderMapper()

    def insert(self, vo: FolderVO):
        try:
            self.mapper.insert(vo)
        except Exception:
            raise CreateException()

    def read_all(self):
        try:
            return self.mapper.read_all()
        except Exception:
            raise ReadException()

    def read(self, folder_id):
        try:
            return self.mapper.read_id(folder_id)
        except Exception:
            raise ReadException()

    def read_location(self, location_id):
        try:
            return self.mapper.read_location(location_id)
        except Exception:
            raise ReadException()

    def update(self, vo: FolderVO):
        try:
            self.mapper.update(vo)
        except Exception:
            raise UpdateException()

    def delete(self, folder_id):
        try:
            self.mapper.delete(folder_id)
        except Exception:
            raise DeleteException()