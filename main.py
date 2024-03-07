import uvicorn
from fastapi import FastAPI
from db_context import SessionLocal, engine, Base
from Controllers import CureController, OrderController, UserController

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(UserController.router, prefix="/user")
app.include_router(CureController.router, prefix="/cure")
app.include_router(OrderController.router, prefix="/order")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.0", port=8000, reload=True, workers=3)

