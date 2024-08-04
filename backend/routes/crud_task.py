from fastapi import APIRouter, HTTPException

from pydantic import ValidationError

from functions.operators import CRUDOperator
from dbmodels import UserCreateModel

crud_task = APIRouter()
crud_operations = CRUDOperator()

@crud_task.get("/api/users")
async def get_all_users():
    response = await crud_operations.read_all_users()
    if response:
        return response
    raise HTTPException(status_code=404, detail="No users found")

@crud_task.get("/api/users/{id}")
async def get_one_user_by_id(id: str):
    response = await crud_operations.read_one_user_by_id(id)
    if response:
        return response
    raise HTTPException(status_code=404, detail="User not found")

@crud_task.post("/api/users", response_model=UserCreateModel)
async def post_user(user: UserCreateModel):
    try:
        email_exists = await crud_operations.read_one_user_by_email(user.email)
        user_exists = await crud_operations.read_one_user_by_name(user.username)
        if user_exists or email_exists:
            raise HTTPException(400, "User with this email already exists")
        
        response = await crud_operations.create_user(user.model_dump())
        if response:
            return response
        raise HTTPException(400, "Something went wrong")
    except ValidationError as e:
        raise HTTPException(422, str(e))
