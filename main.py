from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import schemas
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Conversion Engine API Running 🚀"}


@app.post("/check-phone", response_model=schemas.PhoneCheckResponse)
def check_phone(request: schemas.PhoneCheckRequest, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.phone == request.phone).first()

    if user:
        return {
            "exists": True,
            "user_id": user.user_id
        }

    return {
        "exists": False,
        "user_id": None
    }

@app.post("/create-test-order")
def create_test_order(request: schemas.CreateTestOrderRequest,
                      db: Session = Depends(get_db)):

    # 1️⃣ Create or fetch user
    user = db.query(models.User).filter(models.User.phone == request.phone).first()

    if not user:
        user = models.User(
            phone=request.phone,
            full_name=request.full_name,
            is_phone_verified=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # 2️⃣ Create address
    address = models.Address(
        user_id=user.user_id,
        address_line=request.address_line,
        city=request.city,
        state=request.state,
        pincode=request.pincode
    )
    db.add(address)
    db.commit()
    db.refresh(address)

    # 3️⃣ Calculate totals
    subtotal = sum(item.price * item.quantity for item in request.items)
    total_amount = subtotal + request.delivery_charge

    # 4️⃣ Create order
    order = models.Order(
        user_id=user.user_id,
        address_id=address.address_id,
        subtotal=subtotal,
        delivery_charge=request.delivery_charge,
        total_amount=total_amount
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # 5️⃣ Insert order items
    for item in request.items:
        order_item = models.OrderItem(
            order_id=order.order_id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price,
            total_price=item.price * item.quantity
        )
        db.add(order_item)

    db.commit()

    return {
        "message": "Test order created successfully",
        "order_id": order.order_id,
        "user_id": user.user_id
    }

@app.get("/orders-detailed", response_model=list[schemas.OrderDetailedGridResponse])
def get_orders_detailed(db: Session = Depends(get_db)):

    results = (
        db.query(
            models.Order.order_id,
            models.User.full_name,
            models.User.phone,
            models.Address.address_line,
            models.Address.city,
            models.Address.state,
            models.Address.pincode,
            models.Order.created_at,
            models.Product.product_name,
            models.OrderItem.quantity,
            models.OrderItem.price,
            models.Order.total_amount
        )
        .join(models.User, models.Order.user_id == models.User.user_id)
        .join(models.Address, models.Order.address_id == models.Address.address_id)
        .join(models.OrderItem, models.Order.order_id == models.OrderItem.order_id)
        .join(models.Product, models.OrderItem.product_id == models.Product.product_id)
        .order_by(models.Order.created_at.desc())
        .all()
    )

    return [
        {
            "order_id": r.order_id,
            "customer_name": r.full_name,
            "contact_number": r.phone,
            "full_address": f"{r.address_line}, {r.city}, {r.state}, {r.pincode}",
            "payment_method": None,  # Add payment join later if needed
            "ordered_date": r.created_at,
            "product_name": r.product_name,
            "quantity": r.quantity,
            "price": float(r.price),
            "total_bill": float(r.total_amount)
        }
        for r in results
    ]