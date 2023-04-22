from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.address import Address, Base


# Define the database URL for SQLite
DATABASE_URL = "sqlite:///./address_book.db"

# Create a database engine with the defined URL
engine = create_engine(DATABASE_URL)

# Create all the defined database models in the engine
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    '''
    This function is return the db connection.
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()