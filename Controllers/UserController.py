from fastapi import APIRouter, Depends, HTTPException, Responsefrom sqlalchemy.orm import Sessionfrom db_context import get_dbfrom Services import UserServicefrom ContractModel.user import User as ctUserfrom DatabaseModel.user import User as dbUserdef map_user(db_user: dbUser) -> ctUser:    return ctUser(        uid=db_user.uid,        phoneNumber=db_user.phoneNumber,        name=db_user.name,        address=db_user.address    )router = APIRouter()@router.post("/register", tags=["User"])async def register_user(phoneNumber: int, name: str, address: str, db: Session = Depends(get_db)) -> str:    try:        created_user_uid = UserService.register(phoneNumber, name, address, db)        return created_user_uid    except Exception as e:        print(e)        raise HTTPException(status_code=400, detail="Failed to create user")@router.post("/login", tags=["User"])async def login(phone_number: int, db: Session = Depends(get_db)) -> str:    user = UserService.login(phone_number, db)    if user:        return user.uid    else:        raise HTTPException(status_code=404, detail="User not found")@router.get("/get",tags=["User"], response_model=ctUser)async def get_user(user_uid: str, db: Session = Depends(get_db)) -> ctUser:    db_user = UserService.get_user(user_uid, db)    if db_user:        return map_user(db_user)    else:        raise HTTPException(status_code=404, detail="User not found")@router.delete("/delete", tags=["User"])async def delete_user(user_uid: str, db: Session = Depends(get_db)) -> str:    is_deleted = UserService.delete_user(user_uid, db)    if is_deleted:        return "User deleted successfully"    else:        raise HTTPException(status_code=404, detail="User not found")