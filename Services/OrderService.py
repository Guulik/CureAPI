from typing import List, Optional
from DatabaseModel.order import Order as dbOrder
from DatabaseModel.user import User as dbUser
from DatabaseModel.cure import Cure as dbCure
from DatabaseModel.cure_in_order import CureInOrder as cartCure
from sqlalchemy.orm import Session

import uuid

nullUid: str = str(uuid.UUID(int=0))
cart: list[cartCure] = []


def add_cure(cure_uid: str, user_uid: str, db: Session) -> str:
    try:
        user: dbUser = db.query(dbUser).filter_by(uid=user_uid).first()
        cart: list[cartCure] = db.query(cartCure).filter_by(order_id=None).filter(cartCure.user_id==user.id).all()
        cure: dbCure = db.query(dbCure).filter(dbCure.uid == cure_uid).first()

        cure_in_cart: cartCure | None = None

        for cure_cart in cart:
            if cure_cart.id == cure.id:
                cure_in_cart = cure_cart

        if cure_in_cart is None:
            cure_in_cart: cartCure = cartCure(name=cure.name, cure_id=cure.id,user_id=user.id,
                                              count=1, price=cure.price,
                                              delivery_time=cure.availabilityTime)
            cart.append(cure_in_cart)

            db.add(cure_in_cart)
            db.commit()
        else:
            setattr(cure_in_cart, "count", cure_in_cart.count+1)
            setattr(cure_in_cart, "price", cure_in_cart.count*cure.price)

    except Exception as e:
        print(e)
        return nullUid


def remove_cure(cure_uid: str, user_uid: str, db: Session) -> str:
    try:
        user: dbUser = db.query(dbUser).filter_by(uid=user_uid).first()
        cart: list[cartCure] = db.query(cartCure).filter_by(order_id=None).filter(cartCure.user_id == user.id).all()
        cure: dbCure = db.query(dbCure).filter(dbCure.uid == cure_uid).first()

        cure_in_cart: cartCure | None = None

        for cure_cart in cart:
            if cure_cart.id == cure.id:
                cure_in_cart = cure_cart

        if cure_in_cart.count == 1:
            cart.remove(cure_in_cart)
            db.delete(cure_in_cart)
        else:
            setattr(cure_in_cart, "count", cure_in_cart.count - 1)
            setattr(cure_in_cart, "price", cure_in_cart.count * cure.price)
        db.commit()

    except Exception as e:
        print(e)
        return None


def place_order(cure_uids: List[str], db: Session) -> str:
    new_order_uid = uuid.uuid4()

    order = dbOrder(uid=str(new_order_uid))

    try:
        for cure_uid in cure_uids:
            cure = db.query(dbCure).filter(dbCure.uid == cure_uid).first()
            if cure:
                order.cures.append(cure)
            else:
                raise ValueError(f"Cure with uid {cure_uid} does not exist.")

        db.add(order)
        db.commit()
        db.refresh(order)
        return order.uid
    except Exception as e:
        print(e)
        return nullUid


def get_order(order_id: int, db: Session) -> Optional[dbOrder]:
    try:
        return db.query(dbOrder).filter(dbOrder.id == order_id).first()
    except Exception as e:
        print(e)
        return None


def get_cart(user_uid: str, db: Session) -> Optional[list[cartCure]]:
    try:
        user: dbUser = db.query(dbUser).filter_by(uid=user_uid).first()
        if user:
            cart: list[cartCure] = db.query(dbOrder).filter(dbOrder.user_id == user.id).all()
        else:
            return None
        return cart
    except Exception as e:
        print(e)
        return None
