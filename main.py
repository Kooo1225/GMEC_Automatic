from fastapi import FastAPI, Depends, APIRouter
from fastapi.responses import JSONResponse

from src.controller.FolderController import battery
from src.controller.LocationController import location

app = FastAPI()
app.include_router(battery)
app.include_router(location)

@app.get("/")
def read_root():
    a = {'text': "Hello"}
    return JSONResponse(content=a)
