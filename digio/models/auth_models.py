# GiG


from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# to get a string like this run:
# openssl rand -hex 32
# SECRET_KEY = "018d55df26d269ec31347f0efd532da70f750dbbce8c638c3b42757bdd2674fc"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 5
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(
#             minutes=ACCESS_TOKEN_EXPIRE_MINUTES
#         )
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": False,
#     }
# }


# class Token(BaseModel):
#     access_token: str
#     token_type: str


# class TokenData(BaseModel):
#     username: str | None = None


# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None


# class UserInDB(User):
#     hashed_password: str


# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)


################TODO
# 1. Add response_model to everything?
################TODO


# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except jwt.ExpiredSignatureError as exc:
#         print("in ExpiredSignatureError")
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="token has expired"
#         ) from exc
#     except JWTError as exc:
#         print("JWTError exception", exc)
#         raise credentials_exception from exc
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         print("No user found exception")
#         raise credentials_exception
#     return user


# # @app.post("/token")
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
# ) -> Token:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Incorrect username or password",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         print("at the start", form_data)
#         user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#         if not user:
#             raise credentials_exception
#         access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#         access_token = create_access_token(
#             data={"sub": user.username}, expires_delta=access_token_expires
#         )
#         return Token(access_token=access_token, token_type="bearer")
#     except Exception as exc:
#         print("Got exception ", exc)
#         raise credentials_exception


# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     return current_user


# async def read_own_items(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]