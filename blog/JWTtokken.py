from datetime import datetime, timedelta , timezone
from jose import jwt , JWTError
from . import schemas
from blog.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            print(f"email in verify_token: {email}")
            if email is None:
                print("Email not found in token payload")
                raise credentials_exception
            token_data = schemas.TokenData(email=email)
            print(f"token_data: {token_data}")
            return token_data
        except JWTError:
            raise credentials_exception