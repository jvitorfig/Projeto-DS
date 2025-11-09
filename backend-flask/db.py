from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg://user:password@localhost:5432/meubanco"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)