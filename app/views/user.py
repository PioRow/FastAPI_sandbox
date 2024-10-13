from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.database import get_db

from app.models.user import User as UserModel

router = APIRouter(prefix="/user", tags=["user"])


class UserSchemaBase(BaseModel):
    email:str
    username:str
    password:str

class UserSchemaCreate(UserSchemaBase):
    pass


class UserSchema(UserSchemaBase):
    id: int

    class Config:
        orm_mode = True


@router.get("/get-user", response_model=UserSchema)
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    user = await UserModel.get(db, id)
    return user


@router.get("/get-users", response_model=list[UserSchema])
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await UserModel.get_all(db)
    return users


@router.post("/create-user", response_model=UserSchema)
async def create_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_db)):
    user = await UserModel.create(db, **user.dict())
    return user