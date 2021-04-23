from sqlalchemy.orm import Session
import models, schemas
import uuid

# users
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_email_and_password(db: Session, email: str, password: str):
    return db.query(models.User).filter(models.User.email == email, models.User.password == password).first()

def create_user(db: Session, user: schemas.User):
    uuid_id = uuid.uuid4().hex
    db_user = models.User(id=uuid_id, email=user.email, name=user.name, password=user.password, admin=user.admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_user: schemas.User, update_user: schemas.UpdateUser):

    update_data = update_user.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user





# vendors
def get_vendor(db: Session, vendor_id: int):
    return db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()

def get_vendor_products(db: Session, vendor_id: int):
    return db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first().products

def create_vendor(db: Session, vendor: schemas.Vendor):
    db_vendor = models.Vendor(email=vendor.email, name=vendor.name, package=vendor.package)
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor

def get_vendor_by_email(db: Session, email: str):
    return db.query(models.Vendor).filter(models.Vendor.email == email).first()

def update_vendor(db: Session, db_vendor: schemas.Vendor, update_vendor: schemas.UpdateVendor):

    update_data = update_vendor.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_vendor, key, value)

    db.commit()
    db.refresh(db_vendor)
    return db_vendor





# products
def create_product(db: Session, product: schemas.Product, vendor: models.Vendor):
    db_product = models.Product(category=product.category, subcategory=product.subcategory, description=product.description, vendor=vendor)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session):
    return db.query(models.Product).all()


def get_product(db: Session, product_id):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def update_product(db: Session, db_product: schemas.Product, update_product: schemas.UpdateProduct):

    update_data = update_product.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product
