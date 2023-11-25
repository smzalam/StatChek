import uvicorn
print(__name__)
if __name__ == "__main__":
    uvicorn.run("plinkAPI.src.server.app:app", host="127.0.0.1", port=8000)