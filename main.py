from fastapi import FastAPI
from typing import Union, Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    des: Optional[str] = None
    price: float
    tax: Optional[float] = None

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello" : "World"}

@app.get("/items/{item_id}/{q}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post('/items')
async def create_item(item: Item):
    return item