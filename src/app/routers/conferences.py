from fastapi import FastAPI, Response, status, HTTPException, Depends

@app.get("/conferences")
@app.get("/conferences/{conference_id}")
@app.get("/conferences/{conference_id}/divisions")
@app.get("/conferences/{conference_id}/teams")
