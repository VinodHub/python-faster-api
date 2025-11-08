from typing import List

from fastapi import APIRouter
from fastapi import status, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from product import models
from product.database import get_db
from product.routers.login import get_current_user
from product.schemas import Product, DisplayProduct, Seller

router = APIRouter(tags=["products"],prefix="/product")

@router.post("/add", status_code=status.HTTP_201_CREATED)
def add(product: Product, db: Session = Depends(get_db)):
    new_product = models.Product(name=product.name,
                                 description=product.description,
                                 price=product.price,
                                 seller_id=1)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return product


@router.get("/info", response_model=List[DisplayProduct])
def products(db: Session = Depends(get_db),current_user:Seller =Depends(get_current_user)):
    products_description = db.query(models.Product).all()
    return products_description


@router.get("/{product_id}", response_model=DisplayProduct)
def products(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.delete("/{product_id}")
def delete(product_id: int, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == product_id).delete(synchronize_session=False)
    db.commit()
    return f'Product {product_id} deleted'


@router.put("/{product_id}")
def update(product_id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id)
    if not db_product.first():
        pass
    else:
        db_product.update(product.model_dump())
        db.commit()
    return f'Product {product_id} updated'
