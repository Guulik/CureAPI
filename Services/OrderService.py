import datetime
from typing import List, Optional
from DatabaseModel.order import Order as dbOrder
from DatabaseModel.user import User as dbUser
from DatabaseModel.cure import Cure as dbCure
from DatabaseModel.cure_in_order import CureInOrder as cartCure
from sqlalchemy.orm import Session

import uuid

nullUid: str = str(uuid.UUID(int=0))


def add_cure(cure_uid: str, user_uid: str, db: Session) -> Optional[cartCure]:
    try:
        user: Optional[dbUser] = db.query(dbUser).filter_by(uid=user_uid).first()
        cart = get_cart(user_uid, db)
        cure: dbCure = db.query(dbCure).filter(dbCure.uid == cure_uid).first()

        cure_in_cart: cartCure | None = None

        for cure_cart in cart:
            if cure_cart.cure_id == cure.id:
                cure_in_cart = cure_cart

        if cure_in_cart is None:
            cure_in_cart: cartCure = cartCure(name=cure.name, cure_id=cure.id,user_id=user.id,
                                              count=1, price=cure.price,
                                              delivery_time=cure.availabilityTime)
            cart.append(cure_in_cart)

            db.add(cure_in_cart)
        else:
            setattr(cure_in_cart, "count", cure_in_cart.count+1)
            setattr(cure_in_cart, "price", cure_in_cart.count*cure.price)

        db.commit()
        return cure_in_cart
    except Exception as e:
        print(e)
        return None


def remove_cure(cure_uid: str, user_uid: str, db: Session) -> Optional[cartCure]:
    try:
        cart = get_cart(user_uid, db)
        cure: dbCure = db.query(dbCure).filter(dbCure.uid == cure_uid).first()

        cure_in_cart: cartCure | None = None

        for cure_cart in cart:
            if cure_cart.cure_id == cure.id:
                cure_in_cart = cure_cart

        if cure_in_cart.count == 1:
            cart.remove(cure_in_cart)
            db.delete(cure_in_cart)
        else:
            setattr(cure_in_cart, "count", cure_in_cart.count - 1)
            setattr(cure_in_cart, "price", cure_in_cart.count * cure.price)
        db.commit()
        return cure_in_cart

    except Exception as e:
        print(e)
        return None


def place_order(user_uid: str, delivery_type: bool, db: Session) -> str:
    new_order_uid = str(uuid.uuid4())

    try:
        user: Optional[dbUser] = db.query(dbUser).filter_by(uid=user_uid).first()
        cart = get_cart(user_uid, db)
        newOrder = dbOrder(uid=new_order_uid, price_sum=0, user_id=user.id, delivery_type=delivery_type, timestamp=datetime.datetime.now())

        db.add(newOrder)
        db.commit()
        db.refresh(newOrder)

        for cureInCart in cart:
            setattr(cureInCart, "order_id", newOrder.id)
            setattr(newOrder, "price_sum", newOrder.price_sum+cureInCart.price)
            cure: Optional[dbCure] = db.query(dbCure).filter_by(id=cureInCart.cure_id).first()
            db.commit()
            db.refresh(newOrder)
            setattr(cure, "count", cure.count - cureInCart.count)
            db.commit()

        return newOrder.uid
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
        user: Optional[dbUser] = db.query(dbUser).filter_by(uid=user_uid).first()
        if user:
            cart: list[cartCure] = db.query(cartCure).filter_by(order_id=None).filter(cartCure.user_id == user.id).all()
        else:
            return None
        return cart
    except Exception as e:
        print(e)
        return None
