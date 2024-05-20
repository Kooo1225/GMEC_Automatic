from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.service.LocationService import LocationService
from src.dto.LocationDTO import *
from src.db.connection import get_db


location = APIRouter(prefix='/battery/location')
service = LocationService()

@location.get("/", tags=['location'], response_model=list[LocationDTO])
def read_all(db: Session = Depends(get_db)):
    return service.read_all(db)