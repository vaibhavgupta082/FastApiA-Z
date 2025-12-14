from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status ,Depends
from .import JWTtokken, schemas


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # return JWTtokken.verify_token(data, credentials_exception)
    user = JWTtokken.verify_token(data, credentials_exception)
    print(f"user in get_current_user: {user}")

    if user is None:   # safety net
        raise credentials_exception
    return user