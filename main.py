from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session,engine
import databse_model
from sqlalchemy.orm import Session

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods=["*"]
)

databse_model.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return " Welcome to telusko trac"

products = [
    Product(id=1, name="Phone",  description="A Smartphone",price= 999.99,quantity=5),
    Product(id=2, name="Laptops",  description="A Powerful Laptop", price= 9999.1, quantity=8),
    Product(id=3, name="TV",  description="A SmartTv",price= 978.0, quantity=13),
    Product(id=4, name="Charager",  description="A Fast Charger",  price=9.7,quantity=11),
    Product(id=5, name="Pen",  description="A Writer Pen",price= 1.0,quantity=7),

]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = session()
    count = db.query(databse_model.Product).count()
    
    if count == 0:
        for product in products:
            db.add(databse_model.Product(**product.model_dump()))
        db.commit()

init_db()
 
@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(databse_model.Product).all()
    return db_products

@app.get("/product/{id}")
def get_product_by_id(id:int, db: Session = Depends(get_db)):
    db_product = db.query(databse_model.Product).filter(databse_model.Product.id==id).first()
    if db_product:
        return db_product
    return "product  not found"

@app.post("/products")
def add_product(product : Product,db: Session = Depends(get_db)):
    db.add(databse_model.Product(**product.model_dump()))
    db.commit()
    return product
    
@app.put("/products/{id}")
def update_product(id: int, product : Product,db: Session = Depends(get_db)):
    db_product = db.query(databse_model.Product).filter(databse_model.Product.id==id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "product updated sucessffully"
    else:
     return "product not found"  

@app.delete("/products/{id}")
def delete_product(id : int,db: Session = Depends(get_db)):
        db_product = db.query(databse_model.Product).filter(databse_model.Product.id==id).first()
        if db_product:
            db.delete(db_product)
            db.commit()
            return "product deleted sucessfully"
        else:
            return "product not found"