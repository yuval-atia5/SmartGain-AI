from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load secrets from .env file
load_dotenv()

# Read the database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# The engine is the single connection to PostgreSQL
# Think of it as the phone line to the database
# Created once when the app starts, reused for every request
engine = create_engine(DATABASE_URL)

# sessionmaker returns a class with your settings baked in
# autocommit=False → you control when data saves (all or nothing)
# autoflush=False  → you control when changes sync
# bind=engine      → use this connection for all sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# declarative_base() returns a parent class with database superpowers
# every model will inherit from this Base
# it gives models: table creation, column mapping, registry
Base = declarative_base()

# This function gives each API request its own private session
# yield pauses here and gives db to the request
# finally guarantees db.close() runs no matter what happens
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()