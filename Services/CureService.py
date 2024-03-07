from typing import Type
from DatabaseModel.cure import Cure as dbCure
from sqlalchemy.orm import Session

import uuid


nullUid = str(uuid.UUID(int=0))


def get_cures(db: Session) -> list[Type[dbCure]] | None:
    cures: list[Type[dbCure]] = list(db.query(dbCure).all())
    return cures


def get_cure(cure_uid: str, db: Session) -> dbCure | None:
    return db.query(dbCure).filter(dbCure.uid == cure_uid).first()


def create_cure(name: str, description: str, price: int, count: int, availabilityTime: int,
                db: Session) -> str:
    # random uuid
    new_uid = str(uuid.uuid4())

    cure = dbCure(
        uid=str(new_uid),
        name=name,
        description="" if description is None else description,
        price=price,
        count=count,
        availabilityTime=availabilityTime)

    try:
        db.add(cure)
        db.commit()
        db.refresh(cure)
        return cure.uid
    except Exception as e:
        print(e)
        return nullUid


def edit_cure(cureUid: str, db: Session, **kwargs) -> bool:
    cure = db.query(dbCure).filter(dbCure.uid == cureUid).first()
    if cure is None:
        return False

    for attr, value in kwargs.items():
        if hasattr(cure, attr) and value is not None:
            setattr(cure, attr, value)

    db.commit()
    return True


def remove_cure(cureUid: str, db:Session) -> bool:
    try:
        cure = db.query(dbCure).filter(dbCure.uid == cureUid)
        cure.delete()
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False
