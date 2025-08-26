
import pandas as pd
import numpy as np
import random as rd
import logging
import math
import os
import logging
import statistics

import logging

from fastapi import FastAPI, HTTPException, APIRouter, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

@asynccontextmanager
async def router_lifespan(app: APIRouter):
    global stats
    current_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        yield
    finally:
        pass

router = APIRouter(lifespan=router_lifespan)

@router.get("/rb-rankings", response_class=JSONResponse)
def get_qb_rankings(): 
    try: 
        merged = pd.read_csv("data/merged_rb_rankings.csv")
        return merged.to_dict(orient="records")

    except Exception as e: 
        logger.error(f"Error in get_qb_rankings: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")




