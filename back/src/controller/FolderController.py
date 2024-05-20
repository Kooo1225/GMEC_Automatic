from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.service.FolderService import FolderService
from src.dto.FolderDTO import *
from src.db.connection import get_db


battery = APIRouter(prefix='/battery')
service = FolderService()

@battery.get('/', tags=['battery'], response_model=list[FolderDTOinDB])
def read_all(db: Session = Depends(get_db)):
    data = service.read_all(db)
    return data

@battery.get("/folder/{folder_id}", tags=['battery'], response_model=FolderDTOinDB)
def read_id(folder_id: int, db: Session = Depends(get_db)):
    data = service.read_id(folder_id, db)
    return data

@battery.get("/location/{location_id}", tags=['battery'], response_model=list[FolderDTO])
def read_location(location_id: int, db: Session = Depends(get_db)):
    data = service.read_location(location_id, db)
    return data

# insert 하는 구문이라 response_model은 따로 지정해주지 않았음
@battery.post('/add', tags=['battery'])
def insert(dto: InsertFolderDTO, db: Session = Depends(get_db)):
    service.insert(dto, db)

@battery.put("/put", tags=['battery'])
def update(dto: FolderDTOinDB, db: Session = Depends(get_db)):
    service.update(dto, db)

@battery.delete('/delete/{folder_id}', tags=['battery'])
def delete(folder_id: int, db: Session = Depends(get_db)):
    service.delete(folder_id, db)