from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date

BASE = declarative_base()

class ReplacementVO(BASE):
    __tablename__ = 'Replacement_Date'
    replacement_date_id = Column(Integer, primary_key=True)
    replaced_date = Column(Date)
    folder_id = Column(Integer)

    def __init__(self, replaced_date, folder_id, replacement_date_id=None):
        self.replaced_date = replaced_date
        self.folder_id = folder_id
        self.replacement_date_id = replacement_date_id

    def __repr__(self):
        return f'ReplacementVO(replacement_date_id={self.replacement_date_id}, replaced_date={self.replaced_date}, folder_id={self.folder_id}'

