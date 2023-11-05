import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .routers import conferences, divisions, teams, players, users

# from fastapi.params import Body
# from pydantic import BaseModel

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(conferences.router)
app.include_router(divisions.router)
app.include_router(teams.router)
app.include_router(players.router)


async def check_connections():
    while True:
        await asyncio.sleep(600)
        print("check connections")
        pool.check()


@app.get("/")
def root():
    return {"message": "Welcome to the StatChekAPI!"}


@app.get("/status")
def status():
    return {"message": "API is up and running all dandy and fandy!"}


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
