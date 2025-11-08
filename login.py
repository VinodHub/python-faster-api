from datetime import datetime, timedelta

from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from product import models
from product.database import get_db
from product.schemas import Login, TokenData

SECRET_KEY = "8gAzzpO3MGC8A17YtmWTSnKZJYLh/VkEZ1HW2o6PpF1VapKbWfqWhv09xYicCuGW"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter(tags=["login"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/login")
# def login(login: Login,db: Session = Depends(get_db)):
def login(login: OAuth2PasswordRequestForm=Depends(),db: Session = Depends(get_db)):
    dbuser = db.query(models.Seller).filter(models.Seller.username == login.username).first()
    if not dbuser:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found/Invalid username")
    if not pwd_context.verify(login.password, dbuser.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Incorrect password")
    #gen JWT Token
    access_token = generate_token(
        data ={"sub": dbuser.username})
    return {"access_token": access_token,"token_type": "bearer"}

def get_current_user(token:str =Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

