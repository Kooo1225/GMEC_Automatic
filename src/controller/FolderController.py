from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.service.FolderService import FolderService
from src.dto.FolderDTO import *
from src.db.connection import get_db


battery = APIRouter(prefix='/battery')
service = FolderService()

@battery.get('/', tags=['battery'], response_model=list[FolderDTO])
def read_all(db: Session = Depends(get_db)):
    data = service.read_all(db)
    return data

@battery.post('/add', tags=['battery'])
def insert(dto: InsertFolderDTO, db:Session = Depends(get_db)):
    service.insert(dto, db)