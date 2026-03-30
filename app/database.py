from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite per semplicità
SQLALCHEMY_DATABASE_URL = "sqlite:///./healthhub.db"

# Necessario per SQLite (evita problemi di thread)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dipendenza: ogni richiesta API ha la sua sessione DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
