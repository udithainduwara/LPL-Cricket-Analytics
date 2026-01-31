import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from models import Base

load_dotenv()

DATABASE_URL =os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not in .env file")

engine = create_engine(DATABASE_URL, future=True)

Base.metadata.create_all(engine)
print("Database tables created Succsfully.")