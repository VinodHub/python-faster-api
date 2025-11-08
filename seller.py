from fastapi import APIRouter
from fastapi.params import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from product import models
from product.database import get_db
from product.schemas import Seller, DisplaySellers

router = APIRouter(tags=["sellers"],prefix="/sellers")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
@router.post("/", response_model=DisplaySellers)
def create_seller(seller: Seller, db: Session = Depends(get_db)):
    hash_password = pwd_context.hash(seller.password)
    seller_object = models.Seller(username=seller.username,
                                  email=seller.email, password=hash_password)
    db.add(seller_object)
    db.commit()
    db.refresh(seller_object)
    return seller_object
