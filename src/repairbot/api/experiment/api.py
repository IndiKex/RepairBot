from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=130)


@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}!"}


@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    return {
        "message": "User created",
        "user": user.model_dump(),
    }
