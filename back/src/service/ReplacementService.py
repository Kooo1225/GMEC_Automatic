from src.exception.CustomException import *
from src.mapper.ReplacementMapper import ReplacementMapper
from src.vo.ReplacementVO import ReplacementVO


class FolderService:
    mapper = ReplacementMapper()

    def insert(self, vo: ReplacementVO):
        try:
            self.mapper.insert(vo)
        except Exception:
            raise CreateException()

    def read_all(self):
        try:
            return self.mapper.read_all()
        except Exception:
            raise ReadException()

    def read_id(self, replacement_date_id: int):
        try:
            return self.mapper.read_id(replacement_date_id)
        except Exception:
            raise ReadException()

    def read_date(self, replaced_date):
        try:
            return self.mapper.read_date(replaced_date)
        except Exception:
            raise ReadException()

    def read_folder(self, folder_id):
        try:
            return self.mapper.read_folder(folder_id)
        except Exception:
            raise ReadException()

    def update(self, vo: ReplacementVO):
        try:
            self.mapper.update(vo)
        except Exception:
            raise UpdateException()

    def delete(self, replacement_date_id):
        try:
            self.mapper.delete(replacement_date_id)
        except Exception:
            raise DeleteException()