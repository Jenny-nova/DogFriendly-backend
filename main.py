'''
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db import SessionLocal, engine, Base
from models import Place, User  
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DogFriendly API")

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/places")
def get_places(city: str = "", db: Session = Depends(get_db)):
    query = db.query(Place)
    if city:
        query = query.filter(Place.city.ilike(f"%{city}%"))
    return query.all()


class UserCreate(BaseModel):
    username: str
    email: str

@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"id": db_user.id, "username": db_user.username, "email": db_user.email}

'''
'''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def root():
    return {"ok": True}
'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum  # 👈 necesario para que FastAPI funcione en Vercel

app = FastAPI()

# ✅ CORS: permite llamadas desde tu frontend en Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dog-friendly-frontend.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Ruta raíz (para probar el despliegue)
@app.get("/")
def root():
    return {"ok": True}

# ✅ Handler requerido por Vercel (adaptador ASGI -> Lambda)
handler = Mangum(app)

