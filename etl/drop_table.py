from sqlalchemy import create_engine
from database.models import Base

DB_URL = "postgresql+psycopg2://postgres:UdithaInduwara%40200495@localhost:5432/LPL_analytics"
engine = create_engine(DB_URL, future=True)

Base.metadata.drop_all(bind=engine)

print("DONE ✅ Tables dropped")
