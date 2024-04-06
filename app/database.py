from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_USER = "codimd"
DATABASE_PASSWORD = "change_password"
DATABASE_HOST = "0.0.0.0:5432"
DATABASE_NAME = "codimd"

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DATABASE_NAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
