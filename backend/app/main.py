from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .db import get_session, init_db
from .models import StarItem

app = FastAPI(title="STAR Library API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/items", response_model=StarItem)
def create_item(item: StarItem):
    with get_session() as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item


@app.get("/items")
def list_items():
    with get_session() as session:
        items = session.exec(StarItem.select()).all()
        return items


@app.get("/items/{item_id}")
def get_item(item_id: int):
    with get_session() as session:
        item = session.get(StarItem, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
