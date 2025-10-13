from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
from db import get_db
from models import Place, User
from pydantic import BaseModel, EmailStr

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"ok": True}


class UserCreate(BaseModel):
    username: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr


@app.get("/places")
def get_places(city: Optional[str] = Query(None), db: Session = Depends(get_db)):
    if city:
        lugares = db.query(Place).filter(Place.city.ilike(f"%{city}%")).all()
    else:
        lugares = db.query(Place).all()  # Devuelve todos si no hay ciudad
    return [
        {
            "id": p.id,
            "name": p.name,
            "address": p.address,
            "city": p.city,
            "country": p.country
        } for p in lugares
    ]


@app.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Usuario o email ya registrado")

    new_user = User(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
