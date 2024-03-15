from typing import Annotated, Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, status, Path
from cinema_application.models import Room
from cinema_application.database import get_db
from cinema_application.exceptions import NotFoundException
# from cinema_application.routers.auth import get_current_user

router = APIRouter(prefix="/rooms", tags=["rooms"])

DbDependency = Annotated[Session, Depends(get_db)]
# UserDependency = Annotated[dict, Depends(get_current_user)]


class RoomRequest(BaseModel):
    name: str = Field(min_length=3, max_length=120)
    seats: int = Field(gt=0, lt=1000)


class RoomUpdate(BaseModel):
    name: Optional[str] = None
    seats: Optional[str] = None


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(database: DbDependency):
    return database.query(Room).all()


@router.get("/{room_id}", status_code=status.HTTP_200_OK)
async def get_room_by_id(
    database: DbDependency, room_id: int = Path(gt=0)
):
    todo_element = (
        database.query(Room)
        .filter(Room.id == room_id)
        .first()
    )
    if todo_element is None:
        raise NotFoundException
    return todo_element


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(
    # user: UserDependency, database: DbDependency, todo_request: TodoRequest
    database: DbDependency, room_request: RoomRequest
):
    new_todo_element = Room(**room_request.model_dump())

    database.add(new_todo_element)
    database.commit()


@router.put("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_room(
    database: DbDependency,
    room_request: RoomUpdate,
    room_id: int = Path(gt=0),
):
    updatable_todo = (
        database.query(Room)
        .filter(Room.id == room_id)
        .first()
    )
    if not updatable_todo:
        raise NotFoundException

    updatable_todo.update(**room_request.model_dump(exclude_unset=True))

    database.add(updatable_todo)
    database.commit()


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    database: DbDependency, room_id: int = Path(gt=0)
):
    deletable_todo = (
        database.query(Room)
        .filter(Room.id == room_id)
        .first()
    )
    if not deletable_todo:
        raise NotFoundException
    database.delete(deletable_todo)
    database.commit()
