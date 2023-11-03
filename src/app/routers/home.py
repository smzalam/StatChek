from fastapi import FastAPI, Response, status, HTTPException, Depends

@app.get("/")
@app.get("/status")