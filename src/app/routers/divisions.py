from fastapi import FastAPI, Response, status, HTTPException, Depends

@app.get("/divisions")
@app.get("/divisions/{division_id}")
@app.get("/divisions/{division_id}/teams")
