from src.exception.CustomException import *
from src.mapper.UserMapper import UserMapper
from src.vo.UserVO import UserVO


class UserService:
    mapper = UserMapper()

    def insert(self, vo: UserVO):
        try:
            self.mapper.insert(vo)
        except Exception:
            raise CreateException()

    def read_all(self):
        try:
            return self.mapper.read_all()
        except Exception:
            raise ReadException()

    def read_id(self, id: str):
        try:
            return self.mapper.read_id(id)
        except Exception:
            raise ReadException()

    def update(self, vo: UserVO):
        try:
            self.mapper.update(vo)
        except Exception:
            raise UpdateException()

    def delete(self, id):
        try:
            self.mapper.delete(id)
        except Exception:
            raise DeleteException()