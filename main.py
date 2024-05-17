from fastapi import FastAPI, Depends, APIRouter
from fastapi.responses import JSONResponse

from src.controller.FolderController import battery

app = FastAPI()
app.include_router(battery)

@app.get("/")
def read_root():
    a = {'text': "Hello"}
    return JSONResponse(content=a)
