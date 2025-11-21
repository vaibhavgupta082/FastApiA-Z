from fastapi import APIRouter , Depends,HTTPException , status
from .. import schemas , database ,models ,JWTtokken
from datetime import timedelta
from .. hashing import Hash
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(tags=["authentication"])

@router.post("/login",response_model=schemas.Token)
def login(request : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    if not Hash.verify(user.password , request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password")
    #generate token and return
    access_token_expires = timedelta(minutes=JWTtokken.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = JWTtokken.create_access_token(data={"sub": user.email})
    return schemas.Token(access_token=access_token, token_type="bearer")