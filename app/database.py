from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

print(settings.POSTGRES_SVR_USR)
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.POSTGRES_SVR_USR}:{settings.POSTGRES_SVR_PWD}@{settings.POSTGRES_SVR_URL}:{settings.POSTGRES_SVR_PRT}/{settings.POSTGRES_SVR_DB}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,  bind=engine)

Base = declarative_base()

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

