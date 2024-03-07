import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from db_context import get_db
from Services import OrderService
from ContractModel.order import Order as ctOrder
from DatabaseModel.order import Order as dbOrder

nullUid = str(uuid.UUID(int=0))


def map_order(db_order: dbOrder) -> ctOrder:
    return ctOrder(
        uid=db_order.uid,
        id=db_order.id,
        price_sum=db_order.price_sum,
        delivery_type=db_order.delivery_type,
        timestamp=db_order.timestamp
    )


router = APIRouter()


@router.post("/add_cure", tags=["order"])
async def add_cure(cure_uid: str, user_uid:str, db: Session = Depends(get_db)):
    added_cure_uid = OrderService.add_cure(cure_uid, user_uid, db)
    if added_cure_uid != nullUid:
        return Response(content="Cure added successfully", status_code=200)
    else:
        return Response(content="Failed to add cure to order", status_code=400)


@router.delete("/remove_cure", tags=["order"])
async def remove_cure(cure_uid: str, user_uid:str, db: Session = Depends(get_db)):
    if OrderService.remove_cure(cure_uid, user_uid, db):
        return Response(content="Cure removed successfully", status_code=200)
    else:
        return Response(content="Failed to remove cure from order", status_code=400)


@router.post("/place_order", tags=["order"])
async def place_order(cure_uids: List[str], db: Session = Depends(get_db)):
    new_order_uid = OrderService.place_order(cure_uids, db)
    if new_order_uid != nullUid:
        return new_order_uid
    else:
        return Response(content="Failed to create order", status_code=400)


@router.get("/get_order", tags=["order"])
async def get_order(order_id: int, db: Session = Depends(get_db)):
    order = OrderService.get_order(order_id, db)
    if order:
        return order
    else:
        raise HTTPException(status_code=404, detail="Order not found")
