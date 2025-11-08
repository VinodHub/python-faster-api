from typing import Optional
from pydantic import BaseModel


class Product(BaseModel):
    name: str
    description: str
    price: int


class Seller(BaseModel):
    username: str
    email: str
    password: str


class DisplaySellers(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True


class DisplayProduct(BaseModel):
    name: str
    description: str
    seller: DisplaySellers
    price: int

    class Config:
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str]=None







