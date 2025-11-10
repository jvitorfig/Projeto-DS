from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg://postgres:Felipe%4001@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)