from fastapi import FastAPI, Response, status, HTTPException, Depends

@app.get("/teams")
@app.get("/teams/{team_id}")
@app.get("/teams/{team_id}/players")
@app.get("/teams/{team_id}/roster")
@app.get("/teams/{team_id}/stats")
@app.get("/teams/{team_id}/ranks")
@app.get("/teams/{team_id}/links")
@app.get("/teams/{team_id}/schedule")
@app.get("/teams/{team_id}/history")
