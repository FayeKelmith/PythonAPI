from jose import JWTError, jwt
from datetime import datetime, timedelta
# SECRET_KEY
# ALGORITHM
# Expiration time

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):

    # copy of data to be encoded, payload
    to_encode = data.copy()
    # token expiration time
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # update this information to our dictionay which is the payload
    to_encode.update({"exp": expire})

    # then encode it
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
