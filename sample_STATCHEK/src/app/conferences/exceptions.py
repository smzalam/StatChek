from fastapi import Request
from fastapi.responses import JSONResponse


class ConferenceExceptionHandlerBase(Exception):
    def __init__(self, name: str):
        self.name = name
