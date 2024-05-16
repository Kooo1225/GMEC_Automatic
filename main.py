from fastapi import FastAPI, Depends
from typing import Union, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.db.connection import get_db
from src.mapper.FolderMapper import FolderMapper
from src.mapper.LocationMapper import LocationMapper
from src.mapper.ReplacementMapper import ReplacementMapper
from src.mapper.UserMapper import UserMapper


class Item(BaseModel):
    name: str
    des: Optional[str] = None
    price: float
    tax: Optional[float] = None

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello" : "World"}

@app.get("/items/{item_id}")
def read_item(item_id: str, db: Session = Depends(get_db)):
    mapper = UserMapper()
    res = mapper.read_id(item_id, db)
    return res

@app.post('/items')
async def create_item(item: Item):
    return item
