from pydantic import BaseModel
from datetime import datetime
from typing import Union, Optional

class FolderDTO(BaseModel):
    folder_name: str
    location_id: int
    due_date: Optional[datetime]
    marks: Optional[str]

class FolderDTOinDB(FolderDTO):
    folder_id: int

class InsertFolderDTO(FolderDTO):
    pass