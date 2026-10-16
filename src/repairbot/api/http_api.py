import os
from datetime import UTC, datetime, timedelta

import jwt
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import ExpiredSignatureError

from repairbot.api.api_executor import APIExecutor, query_cmd_type, user_cmd_type

app = FastAPI()

api_executor = APIExecutor()

load_dotenv("secrets.env")

# ================
#  BASIC COMMANDS
# ================


@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.get("/health")
def health():
    return {"status": "ok"}


# ===============
#  USER HANDLING
# ===============

SECRET_AUTH_KEY = os.environ["AUTHENTICATION_KEY"]
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def create_access_token(username: str) -> str:
    expires = datetime.now(UTC) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)

    payload = {"sub": username, "exp": expires}

    return jwt.encode(payload, SECRET_AUTH_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_AUTH_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if not isinstance(username, str) or not username:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return username
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=404,
            detail="Expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.post("/users/login")
def login(form: OAuth2PasswordRequestForm = Depends()):  # noqa: B008
    if not api_executor.user_handling(user_cmd_type.AUTH, form.username, form.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token(form.username)

    return {"access_token": token, "token_type": "bearer"}


@app.post("/users/signup")
def signup(form: OAuth2PasswordRequestForm = Depends()):  # noqa: B008
    result: bool = api_executor.user_handling(
        user_cmd_type.ADD, form.username, form.password
    )
    if not result:
        raise HTTPException(
            status_code=401, detail="User already exists with this username"
        )

    token = create_access_token(form.username)

    return {"access_token": token, "token_type": "bearer"}


@app.post("/user/delete")
def delete(form: OAuth2PasswordRequestForm = Depends()):  # noqa: B008
    result: bool = api_executor.user_handling(
        user_cmd_type.REMOVE, form.username, form.password
    )
    if not result:
        raise HTTPException(
            status_code=401, detail="User doesn't exist or wrong password"
        )

    return {"message": "Removed user successfully"}


@app.get("/users/ping/{username}")
def ping_user(username: str, current_username: str = Depends(get_current_user)):
    if username != current_username:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User pinged successfully"}


@app.post("/query/add")
def add_query(question: str, username: str = Depends(get_current_user)):
    query_id = api_executor.query_handling(query_cmd_type.ADD, None, username, question)
    if not query_id:
        raise HTTPException(
            status_code=403,
            detail="Query with query_id already exists. Please try again.",
        )
    return {"message": "Successfully recieved query", "query_id": query_id}


@app.get("/query/get/{query_id}")
def get_query(query_id: str, username: str = Depends(get_current_user)):
    query = api_executor.query_handling(query_cmd_type.GET, query_id, None, None)
    if (
        isinstance(query, dict)
        and isinstance(query["content"], dict)
        and query["content"]["username"] != username
    ):
        raise HTTPException(status_code=404, detail="Query not found")
    return {"message": query}


@app.get("/query/list")
def list_queries(username: str = Depends(get_current_user)):
    query_list = api_executor.query_handling(query_cmd_type.LIST, None, username, None)
    if not query_list:
        raise HTTPException(status_code=404, detail="Queries not found for user")
    return {"message": query_list}
