from fastapi import FastAPI, Response, status, HTTPException, Depends

@app.get("/players/{player_id}")
@app.get("/players/search")
