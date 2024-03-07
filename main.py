import uvicorn
from fastapi import FastAPI
from db_context import SessionLocal, engine, Base
from Controllers import CureController, OrderController, UserController
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserController.router, prefix="/user")
app.include_router(CureController.router, prefix="/cure")
app.include_router(OrderController.router, prefix="/order")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, workers=3)

