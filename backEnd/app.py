
from fastapi import FastAPI, HTTPException 
import uvicorn 

from predict.predictFantasyPoints import router as getPredictions_route 
from rankings.qb_rankings import router as getQBRankings_route

from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

app.include_router(getPredictions_route)
app.include_router(getQBRankings_route)

if __name__ == "__main__":
    try: 
        uvicorn.run(app, host='0.0.0.0', port=8000)
    except Exception as Argument: 
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {Argument}") 
 