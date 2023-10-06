from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# NOTE: format of a connection string we have to pass into sqlalchemy
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:pythonapi123@localhost/pythonapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# the objects of this class are sessions to the db
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# we will later inherit this base class to create db models. I believe schemas.
Base = declarative_base()


# WE CREATE A DEPENDENCY:

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# INFO : All of this is available in fastapi's docs
