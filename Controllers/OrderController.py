import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from db_context import get_db
from Services import OrderService
from ContractModel.order import Order as ctOrder
from ContractModel.cure_in_order import CureInOrder as ctCartCure
from DatabaseModel.order import Order as dbOrder
from DatabaseModel.cure_in_order import CureInOrder as dbCartCure

nullUid = str(uuid.UUID(int=0))


def map_order(db_order: dbOrder) -> ctOrder:
    return ctOrder(
        uid=db_order.uid,
        id=db_order.id,
        price_sum=db_order.price_sum,
        delivery_type=db_order.delivery_type,
        timestamp=db_order.timestamp
    )


def map_cure_in_order(cartCure: dbCartCure) -> ctCartCure:
    return ctCartCure(
        name=cartCure.name,
        count=cartCure.count,
        price=cartCure.price,
        delivery_time=cartCure.delivery_time,
        cure_id=cartCure.cure_id,
        user_id=cartCure.user_id,
        order_id=cartCure.order_id
    )


router = APIRouter()


@router.post("/add_cure", tags=["order"], response_model=ctCartCure)
async def add_cure(cure_uid: str, user_uid:str, db: Session = Depends(get_db)):
    added_cure = OrderService.add_cure(cure_uid, user_uid, db)
    if added_cure:
        return map_cure_in_order(added_cure)
    else:
        return Response(content="Failed to add cure to order", status_code=400)


@router.post("/remove_cure", tags=["order"], response_model=ctCartCure)
async def remove_cure(cure_uid: str, user_uid:str, db: Session = Depends(get_db)):
    removed_cure = OrderService.remove_cure(cure_uid, user_uid, db)
    if removed_cure:
        return map_cure_in_order(removed_cure)
    else:
        return Response(content="Failed to remove cure from order", status_code=400)


@router.post("/place_order", tags=["order"])
async def place_order(user_uid: str, delivery_type: bool, db: Session = Depends(get_db)):
    new_order_uid = OrderService.place_order(user_uid, delivery_type, db)
    if new_order_uid != nullUid:
        return new_order_uid
    else:
        return Response(content="Failed to create order", status_code=400)


@router.get("/get_cart", tags=["order"])
async def get_cart(user_uid: str, db: Session = Depends(get_db)):
    cart = OrderService.get_cart(user_uid, db)
    if cart:
        return cart
    else:
        return {"message": "Cart is empty"}


@router.get("/get_order", tags=["order"])
async def get_order(order_id: int, db: Session = Depends(get_db)):
    order = OrderService.get_order(order_id, db)
    if order:
        return order
    else:
        raise HTTPException(status_code=404, detail="Order not found")
