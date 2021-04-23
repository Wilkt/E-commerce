from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


from database import Base


class User(Base):
	__tablename__ = "users"

	id = Column(String, primary_key=True, index=True)
	# id = Column(String, primary_key=True, unique=True)
	email = Column(String, unique=True, index=True)
	name = Column(String)
	password = Column(String)
	admin = Column(Boolean)

	

class Vendor(Base):
	__tablename__ = "vendors"

	id = Column(Integer, primary_key=True, index=True)
	email = Column(String, unique=True, index=True)
	name = Column(String)
	package = Column(String)

	products = relationship("Product", back_populates="vendor")


	
class Product(Base):
	__tablename__= "products"

	id = Column(Integer, primary_key=True, index=True)
	category = Column(String, index=True)
	subcategory = Column(String, index=True)
	description = Column(String, index=True)
	vendor_id = Column(Integer, ForeignKey("vendors.id"))
	
	vendor = relationship("Vendor", back_populates="products")
	