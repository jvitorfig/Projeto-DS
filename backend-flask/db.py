import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database_url = os.getenv("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql+psycopg2://", 1)
elif database_url and database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+psycopg2://", 1)

if not database_url:
    database_url = "sqlite:///./test.db" 

# 3. Cria o motor com a URL corrigida
engine = create_engine(database_url)

SessionLocal = sessionmaker(bind=engine)