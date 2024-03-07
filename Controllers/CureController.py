from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from DatabaseModel.cure import Cure as dbCure
from ContractModel.cure import Cure as ctCure
from Services import CureService
from db_context import get_db


def map_cure(db_cure) -> ctCure:
    return ctCure(
        uid=db_cure.uid,
        name=db_cure.name,
        description=db_cure.description,
        price=db_cure.price,
        count=db_cure.count,
        availabilityTime=db_cure.availabilityTime
    )


router = APIRouter()


@router.get("/get_all", response_model=list[ctCure])
def get_all_cures(db: Session = Depends(get_db)):
    cures = CureService.get_cures(db)
    return [map_cure(cure) for cure in cures]


@router.get("/get_cure", response_model=ctCure)
def get_cure(cureUid: str, db: Session = Depends(get_db)):
    cure = CureService.get_cure(cureUid, db)
    if cure is None:
        raise HTTPException(status_code=404, detail="Cure not found")
    return map_cure(cure)

@router.post("/create_cure")
def create_cure(name: str,  price: int, count: int, availabilityTime: int, description: str = None, db: Session = Depends(get_db)):
    return CureService.create_cure(name, description, price, count, availabilityTime, db)

@router.put("/edit_cure")
def edit_cure(cureUid: str, name: str = None, description: str = None, price: int = None, count: int = None, availabilityTime: int = None, db: Session = Depends(get_db)):
    success = CureService.edit_cure(cureUid, db, name=name, description=description, price=price, count=count, availabilityTime=availabilityTime)
    if not success:
        raise HTTPException(status_code=404, detail="Cure not found")
    return {"message": "Cure updated successfully"}

@router.delete("/delete_cure")
def delete_cure(cureUid: str, db: Session = Depends(get_db)):
    success = CureService.remove_cure(cureUid, db)
    if not success:
        raise HTTPException(status_code=404, detail="Cure not found")
    return {"message": "Cure deleted successfully"}