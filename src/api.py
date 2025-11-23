from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

from db.crud import DBcrud

app = FastAPI()
db = DBcrud()

items: List[List[int]] = []

class Item(BaseModel):
    text: List[int]

# Static files
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

@app.get("/")
async def serve_demo(request: Request):
    issues = db.get_all_issues()
    for x in issues:
        block = db.get_block(x.i_number)
        x.block = block.content
        x.response = block.response
    return templates.TemplateResponse("home.html", {"request": request, "issues":issues})

@app.delete("/delete-db")
async def delete_db(request: Request):
    db.delete_all()
    return {"status": "ok", "items": items}

@app.get("/items")
async def get_items():
    return items

@app.post("/items")
async def add_item(item: Item):
    items.append(item.text)
    return {"status": "ok", "items": items}

@app.delete("/items/{index}")
async def delete_item(index: int):
    try:
        items.pop(index)
        return {"status": "deleted", "items": items}
    except IndexError:
        raise HTTPException(status_code=404, detail="Item not found")