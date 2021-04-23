from pydantic import BaseModel
from typing import Optional

class LoginUser(BaseModel):
	email: str
	password: str

class User(BaseModel):
    name: str
    email: str
    password: str
    admin: bool

class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    admin: Optional[bool] = None

class Vendor(BaseModel):
    name: str
    email: str
    package: str

class UpdateVendor(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    package: Optional[str] = None


class Product(BaseModel):
	category: str
	subcategory: str
	description: str
	vendor_id: int

class UpdateProduct(BaseModel):
    category: Optional[str] = None
    subcategory: Optional[str] = None
    description: Optional[str] = None
    vendor_id: Optional[int] = None

