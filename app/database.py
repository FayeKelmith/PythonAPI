from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# NOTE: format of a connection string we have to pass into sqlalchemy
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

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

# NO longer useful:

# INFO: we have to write
# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost', database='pythonapi', user='postgres', password='pythonapi123', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("We got to the database")
#         break

#     except Exception as error:
#         print(f'We ran into an error {error}')
