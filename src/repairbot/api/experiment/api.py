import os
from datetime import UTC, datetime, timedelta

import jwt
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel, Field

from repairbot.api.experiment.user_database import UserDatabase

app = FastAPI()

user_database = UserDatabase()

load_dotenv("secrets.env")

SECRET_KEY = os.environ["AUTHENTICATION_KEY"]
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=100)


@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.get("/health")
def health():
    return {"status": "ok"}


def create_access_token(username: str) -> str:
    expires = datetime.now(UTC) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)

    payload = {"sub": username, "exp": expires}

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        username = payload.get("sub")

        print("JWT decoded successfully", flush=True)
        print("Username:", username, flush=True)

        if not isinstance(username, str) or not username:
            raise InvalidTokenError("Missing subject")

        return username

    except InvalidTokenError as exc:
        print("JWT validation failed:", type(exc).__name__, flush=True)

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends()):  # noqa: B008
    if not user_database.authenticate(
        {"username": form.username, "password": form.password}
    ):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token(form.username)

    return {"access_token": token, "token_type": "bearer"}


from uuid import uuid4

query_db: dict[str, dict[str, str]] = {}


class QueryRequest(BaseModel):
    question: str


@app.post("/queries")
def create_query(request: QueryRequest, username: str = Depends(get_current_user)):

    query_id = str(uuid4())

    answer = f"Answer to {request.question}"

    query_db[query_id] = {
        "owner": username,
        "question": request.question,
        "answer": answer,
    }

    return {"query_id": query_id, "answer": answer}


@app.get("/queries/{query_id}")
def get_query(query_id: str, username: str = Depends(get_current_user)):
    query = query_db[query_id]

    if not query or query["owner"] != username:
        raise HTTPException(status_code=404, detail="Query not found")

    return {
        "query_id": query_id,
        "question": query["question"],
        "answer": query["answer"],
    }
