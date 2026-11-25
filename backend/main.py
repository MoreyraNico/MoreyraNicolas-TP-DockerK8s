import socket
import os
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# ==========================================
# 1. CONEXIÓN A BASE DE DATOS (PostgreSQL)
# ==========================================
DB_USER = os.getenv("POSTGRES_USER", "admin")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "usuarios_db")

DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==========================================
# 2. MODELO DE TABLA (Equivalente a @Entity)
# ==========================================
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

Base.metadata.create_all(bind=engine)

# ==========================================
# 3. ESQUEMAS DE VALIDACIÓN (Equivalente a DTOs)
# ==========================================
class UserBase(BaseModel):
    nombre: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

# ==========================================
# 4. APLICACIÓN FASTAPI Y CORS
# ==========================================
app = FastAPI(title="API CRUD Usuarios")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

# ==========================================
# 5. ENDPOINTS CRUD (POST, GET, PUT, DELETE)
# ==========================================
@app.get("/")
def health_check():
    return {"status": "ok", "mensaje": "API FastAPI corriendo",  "backend_replica": socket.gethostname()}

@app.post("/users", response_model=UserResponse, status_code=201)
def crear_usuario(user: UserCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(UserDB).filter(UserDB.email == user.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    nuevo_usuario = UserDB(nombre=user.nombre, email=user.email)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@app.get("/users", response_model=List[UserResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(UserDB).order_by(UserDB.id.asc()).all()

@app.put("/users/{user_id}", response_model=UserResponse)
def actualizar_usuario(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    usuario = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    email_ocupado = db.query(UserDB).filter(
        UserDB.email == user_data.email, 
        UserDB.id != user_id
    ).first()
    if email_ocupado:
        raise HTTPException(status_code=400, detail="Ese email ya pertenece a otro usuario")

    usuario.nombre = user_data.nombre
    usuario.email = user_data.email
    db.commit()
    db.refresh(usuario)
    return usuario

@app.delete("/users/{user_id}", status_code=204)
def eliminar_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()
    return None
