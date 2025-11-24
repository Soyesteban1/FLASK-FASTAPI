# models.py
from sqlalchemy import Column, Integer, String
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)   # hashed
    rol = Column(String, nullable=False)        # admin | profesor | estudiante

class Estudiante(Base):
    __tablename__ = "estudiantes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    edad = Column(Integer, nullable=False)
    curso = Column(String, nullable=False)

class Profesor(Base):
    __tablename__ = "profesores"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    curso = Column(String, nullable=False)
