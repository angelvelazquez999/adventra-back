import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Configura la URL de la base de datos usando una variable de entorno
# Ejemplo de valor: mysql+pymysql://user:password@localhost:3306/adventra
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@localhost:3306/adventra")

# Crear engine y session factory
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para los modelos
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a SQLAlchemy Session and closes it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
