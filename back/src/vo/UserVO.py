from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

BASE = declarative_base()


class UserVO(BASE):
    __tablename__ = 'User'
    user_id = Column(Integer, primary_key=True)
    id = Column(String)
    password = Column(String)

    def __init__(self, id, password, user_id=None):
        self.user_id = user_id
        self.id = id
        self.password = password

    def __repr__(self):
        return f'UserVO(user_id={self.user_id}, id={self.id}, password={self.password})'