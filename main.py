from fastapi import FastAPI

from product import models
from product.database import engine
from product.routers import product, seller, login

app = FastAPI(title="FasterApi Integration with sqlLite",
              description="FasterAPI Integration with sqlLite",
              terms_of_service="https://www.google.com/policies/get/terms/",
              contact={"email":"vinodkr@test.com"},
               docs_url="/docs",)
app.include_router(product.router)
app.include_router(seller.router)

app.include_router(login.router)

models.Base.metadata.create_all(engine)
