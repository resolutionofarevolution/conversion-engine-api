from sqlalchemy import Column, Integer, BigInteger, String, Boolean, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, index=True)
    phone = Column(String, unique=True, nullable=False)
    full_name = Column(String)
    email = Column(String)
    is_phone_verified = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"))
    address_id = Column(BigInteger, ForeignKey("addresses.address_id"))

    subtotal = Column(Numeric)
    delivery_charge = Column(Numeric)
    total_amount = Column(Numeric)

    order_status = Column(String, default="PLACED")
    payment_status = Column(String, default="PENDING")
    created_at = Column(TIMESTAMP, server_default=func.now())

class Address(Base):
    __tablename__ = "addresses"

    address_id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"))
    address_line = Column(String)
    city = Column(String)
    state = Column(String)
    pincode = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())


class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(BigInteger, primary_key=True, index=True)
    order_id = Column(BigInteger, ForeignKey("orders.order_id"))
    product_id = Column(BigInteger, ForeignKey("products.product_id"))
    quantity = Column(Integer)
    price = Column(Numeric)
    total_price = Column(Numeric)

class Product(Base):
    __tablename__ = "products"

    product_id = Column(BigInteger, primary_key=True, index=True)
    product_name = Column(String)
    price = Column(Numeric)
    stock = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())


