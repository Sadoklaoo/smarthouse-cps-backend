from app.models import Base, engine 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def initialize_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()