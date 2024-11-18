from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from constants.config import ConfigDatabase


DATABASE_URL = f"postgresql://{ConfigDatabase.DB_USER}:{ConfigDatabase.DB_PASSWORD}@{ConfigDatabase.DB_HOST}:{ConfigDatabase.DB_PORT}/{ConfigDatabase.DB_NAME}"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_db_connection():
    try:
        with engine.connect() as connection:
            return {'message': 'Successfully database connection'}
    except SQLAlchemyError as e:
        return {'error': f'Fail database connection: {e}'}