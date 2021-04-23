from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException

from database import SessionLocal, engine
from pydantic import BaseModel
import schemas, crud, models
import jwt

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


jwt_secret = "secret"

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


@app.post("/login")
def login(user: schemas.LoginUser, db: Session = Depends(get_db)):
	decoded_password = jwt.decode(user.password, jwt_secret, algorithms=["HS256"])
	password = decoded_password["password"]
	db_user = crud.get_user_by_email_and_password(db, email=user.email, password=password)
	
	if db_user:
		return { "message": f"Successful login: {db_user.name}" }
	else:
		raise HTTPException(status_code=400, detail="Wrong email or password")


# users
@app.post("/user", response_model=schemas.User)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
	db_user = crud.get_user_by_email(db, email=user.email)

	if db_user:
		raise HTTPException(status_code=400, detail="Email already exists")
	else:
		db_user = crud.create_user(db=db, user=user)

	jwt_password = jwt.encode({"password": db_user.password}, jwt_secret, algorithm="HS256")

	return { "user_id": db_user.id, "name": db_user.name, "email": db_user.email, "password": jwt_password, "admin": db_user.admin }


@app.get("/user/me")
def get_me(token: str, db: Session = Depends(get_db)):
	decoded_token = jwt.decode(token, jwt_secret, algorithms=["HS256"])
	user_id = decoded_token["user_id"]

	if user_id:
		return crud.get_user(db, user_id)
	else:
		raise HTTPException(status_code=400, detail="User does not exist")


@app.get("/user/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_db)):
	db_user = crud.get_user(db, user_id)

	if db_user:
		return crud.get_user(db, user_id)
	else:
		raise HTTPException(status_code=400, detail="User does not exist")


@app.put("/user/{user_id}")
def update_user(update_user: schemas.UpdateUser, user_id: str, db: Session = Depends(get_db)):
	db_user = crud.get_user(db, user_id)

	if db_user:
		return crud.update_user(db=db, db_user=db_user, update_user=update_user)
	else:
		raise HTTPException(status_code=400, detail="User does not exist")



@app.get("/get_user_token/{user_id}")
def get_user_token(user_id: str, db: Session = Depends(get_db)):
	db_user = crud.get_user(db, user_id)

	if db_user:
		user = crud.get_user(db, user_id)
		encoded_token = jwt.encode({"user_id": user.id}, jwt_secret, algorithm="HS256")
		return {"token": encoded_token}
	else:
		raise HTTPException(status_code=400, detail="User does not exist")






# vendors
@app.post("/vendor", response_model=schemas.Vendor)
def create_vendor(vendor: schemas.Vendor, db: Session = Depends(get_db)):
	db_vendor = crud.get_vendor_by_email(db, email=vendor.email)

	if db_vendor:
		raise HTTPException(status_code=400, detail="Email already exists")
	else:
		if vendor.package not in ["gold", "silver", "bronze"]:
			raise HTTPException(status_code=400, detail=f"Wrong package name: {vendor.package}")

		db_vendor = crud.create_vendor(db=db, vendor=vendor)

	return { "user_id": db_vendor.id, "name": db_vendor.name, "email": db_vendor.email, "package": db_vendor.package }


@app.get("/vendor/{vendor_id}/products")
def get_vendor_products(vendor_id: str, db: Session = Depends(get_db)):

	if crud.get_vendor(db, vendor_id):
		vendor_products = crud.get_vendor_products(db=db, vendor_id=vendor_id)
	else:
		raise HTTPException(status_code=400, detail=f"Vendor id: {vendor_id} does not exist")

	return {"products": [{ "product_id": vendor_product.id, "product_category": vendor_product.category, "product_subcategory": vendor_product.subcategory } for vendor_product in vendor_products]}

@app.get("/vendor/{vendor_id}")
def get_vendor(vendor_id: str, db: Session = Depends(get_db)):
	return crud.get_vendor(db, vendor_id)


@app.put("/vendor/{vendor_id}")
def update_vendor(update_vendor: schemas.UpdateVendor, vendor_id: str, db: Session = Depends(get_db)):
	db_vendor = crud.get_vendor(db, vendor_id)
	return crud.update_vendor(db=db, db_vendor=db_vendor, update_vendor=update_vendor)








# products
@app.get("/products")
def get_products(db: Session = Depends(get_db)):
	products = crud.get_products(db)
	return { "products": products }



@app.get("/product/{product_id}")
def get_product(product_id: str, db: Session = Depends(get_db)):
	return crud.get_product(db, product_id)


@app.post("/product", response_model=schemas.Product)
def create_product(product: schemas.Product, db: Session = Depends(get_db)):
	vendor_id = product.vendor_id
	vendor = crud.get_vendor(db, vendor_id=vendor_id)

	if vendor:
		db_product = crud.create_product(db=db, product=product, vendor=vendor)
	else:
		raise HTTPException(status_code=400, detail="Vendor does not exist")

	return { "product_id": db_product.id, "category": db_product.category, "subcategory": db_product.subcategory, "description": db_product.description, "vendor_id": vendor_id }



@app.put("/product/{product_id}")
def update_product(update_product: schemas.UpdateProduct, product_id: str, db: Session = Depends(get_db)):
	db_product = crud.get_product(db, product_id)
	return crud.update_product(db=db, db_product=db_product, update_product=update_product)

