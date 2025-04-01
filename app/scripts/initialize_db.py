from sqlalchemy import create_engine
from app.core.database import Base

DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@db:5432/smart_house_db"


def initialize_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.drop_all(bind=engine)  # Drop all existing tables
    Base.metadata.create_all(bind=engine)  # Recreate tables


if __name__ == "__main__":
    initialize_db()
    print("Database initialized successfully.")
