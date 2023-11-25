import asyncio
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from plinkAPI.src.server import auth as auth
from plinkAPI.src.routers.users import router as users
from plinkAPI.src.routers.conferences import router as conferences
from plinkAPI.src.routers.divisions import router as divisions
from plinkAPI.src.routers.teams import router as teams
from plinkAPI.src.routers.players import router as players


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
app.include_router(conferences.router, dependencies=[Depends(auth.valid_current_user)])
app.include_router(divisions.router, dependencies=[Depends(auth.valid_current_user)])
app.include_router(teams.router, dependencies=[Depends(auth.valid_current_user)])
app.include_router(players.router, dependencies=[Depends(auth.valid_current_user)])


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