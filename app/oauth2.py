from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schema, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# SECRET_KEY
# ALGORITHM
# Expiration time

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):

    # copy of data to be encoded, payload
    to_encode = data.copy()
    # token expiration time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # update this information to our dictionay which is the payload
    to_encode.update({"exp": expire})

    # then encode it
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id = str(payload.get("user_id"))

        if id is None:
            raise credentials_exception
        # it's just the user id for now but could be more than that later
        token_data = schema.TokenData(id=id)
        # this is just the id, which is the only payload we have in our token.
        return token_data
    except JWTError:
        raise credentials_exception

# we will use this as a dependency in our path operations and get the current user. it will first call the verify_access_token and check the validity of the token before obtaining the user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    verified_token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(
        models.User.id == verified_token.id).first()

    return user
# All of this is useful in protecting endpoints that need authentication to tbe accessed. So we will add them to our endpoints that need authentication as dependencies/
