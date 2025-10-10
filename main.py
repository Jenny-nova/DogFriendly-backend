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
'''
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db import get_db
from models import Place, User

app = FastAPI()

# CORS para permitir peticiones desde tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O cambia "*" por tu dominio de frontend
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"ok": True}

# Endpoint para listar lugares por ciudad
@app.get("/places")
def get_places(city: str = Query(...), db: Session = Depends(get_db)):
    lugares = db.query(Place).filter(Place.city.ilike(f"%{city}%")).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "address": p.address,
            "city": p.city,
            "country": p.country
        } for p in lugares
    ]

# Endpoint para registrar usuario
@app.post("/register")
def register_user(username: str, email: str, db: Session = Depends(get_db)):
    existing = db.query(User).filter((User.username == username) | (User.email == email)).first()
    if existing:
        return {"error": "Usuario o email ya registrado"}
    
    user = User(username=username, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username, "email": user.email}
'''

'''
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db import get_db
from models import Place, User

app = FastAPI()

# CORS para permitir peticiones desde tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O cambia "*" por tu dominio de frontend
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"ok": True}

# Endpoint para listar lugares, city ahora opcional
@app.get("/places")
def get_places(city: str = Query(None, description="Ciudad para filtrar lugares"), db: Session = Depends(get_db)):
    query = db.query(Place)
    if city:
        query = query.filter(Place.city.ilike(f"%{city}%"))
    lugares = query.all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "address": p.address,
            "city": p.city,
            "country": p.country
        } for p in lugares
    ]

# Endpoint para registrar usuario
@app.post("/register")
def register_user(username: str, email: str, db: Session = Depends(get_db)):
    existing = db.query(User).filter((User.username == username) | (User.email == email)).first()
    if existing:
        return {"error": "Usuario o email ya registrado"}
    
    user = User(username=username, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username, "email": user.email}
'''

'''
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db import get_db
from models import Place, User
from schemas import UserCreate  # Nuevo import

app = FastAPI()

# CORS para permitir peticiones desde tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O cambia "*" por tu dominio de frontend
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"ok": True}

# Endpoint para listar lugares por ciudad
@app.get("/places")
def get_places(city: str = Query(...), db: Session = Depends(get_db)):
    lugares = db.query(Place).filter(Place.city.ilike(f"%{city}%")).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "address": p.address,
            "city": p.city,
            "country": p.country
        } for p in lugares
    ]

# Endpoint para registrar usuario usando JSON en body
@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario o email ya existen
    existing = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if existing:
        return {"error": "Usuario o email ya registrado"}
    
    # Crear nuevo usuario
    new_user = User(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email}
'''

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
from db import get_db
from models import Place, User
from pydantic import BaseModel, EmailStr

app = FastAPI()

# CORS para permitir peticiones desde tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar por el dominio de tu frontend en producción
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"ok": True}

# Schemas para el registro de usuarios
class UserCreate(BaseModel):
    username: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

# Endpoint para listar lugares
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

# Endpoint para registrar usuario
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
