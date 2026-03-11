from fastapi import FastAPI
from app.routers import categories, auth, items, orders, order_items


app = FastAPI()


@app.get('/')
def read_root():
    return {"Hello": "World"}


app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(categories.router, prefix="/api", tags=["categories"])
app.include_router(items.router, prefix="/api", tags=["items"])
app.include_router(orders.router, prefix="/api", tags=["orders"])
app.include_router(order_items.router, prefix="/api", tags=["order-items"])
