from typing import Type, Optional

from DatabaseModel.user import User as dbUser
from sqlalchemy.orm import Session

import uuid


def register(phoneNumber: int, name: str, address: str, db: Session) -> str:
    #random uuid
    new_uid = uuid.uuid4()
    user = dbUser(
        uid=str(new_uid),
        phoneNumber=phoneNumber,
        name=name,
        address=address
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        print(e)

    return str(user.uid)


def login(phone_number: int, db: Session,) -> Optional[dbUser]:
    return db.query(dbUser).filter(dbUser.phoneNumber == phone_number).first()


def get_user(user_uid: str, db: Session) -> Type[dbUser] | None:
    return db.query(dbUser).filter(dbUser.uid == user_uid).first()


def delete_user(user_uid: str, db: Session) -> bool:
    try:
        user = db.query(dbUser).filter(dbUser.uid == user_uid)
        user.delete()
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False
