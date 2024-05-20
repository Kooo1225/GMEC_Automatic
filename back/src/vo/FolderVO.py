from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

BASE = declarative_base()

class FolderVO(BASE):
    __tablename__ = 'Folder'
    folder_id = Column(Integer, primary_key=True)
    folder_name = Column(String)
    location_id = Column(Integer)
    due_date = Column(Date)
    marks = Column(String)

    # def __init__(self, folder_name, location_id, due_date, marks, folder_id=None):
    #     self.folder_id = folder_id
    #     self.folder_name = folder_name
    #     self.location_id = location_id
    #     self.due_date = due_date
    #     self.marks = marks

    def __repr__(self):
        return f"Folder(folder_id={self.folder_id}, folder_name={self.folder_name}, location_id={self.location_id}, due_date={self.due_date})>"


