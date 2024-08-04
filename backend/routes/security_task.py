from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta

from dbmodels import UserModel
from functions.operators import JWTOperator

security_task = APIRouter()
jwt_functions = JWTOperator()

@security_task.get("/api/login/")
async def user_login(user: UserModel = Depends(jwt_functions.validate_token)):
    return user

@security_task.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await jwt_functions.authenticate_user(form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=30)
    access_token_jwt = await jwt_functions.create_token({"sub": user["username"]}, time_expires=access_token_expires)
    return {
        "access_token": access_token_jwt,
        "token_type": "bearer",
    }