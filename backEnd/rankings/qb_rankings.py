
import pandas as pd
import numpy as np
import random as rd
import logging
import math
import os
import logging
import statistics

from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def router_lifespan(app: APIRouter):
    global stats
    current_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        yield
    finally:
        pass

router = APIRouter(lifespan=router_lifespan)
router.mount("/frontEnd/css", StaticFiles(directory="frontEnd/css"), name="static")

@router.get("/qb-rankings", response_class = JSONResponse)
def get_qb_rankings():
    primary_qb_rankings = pd.read_csv("data/qb_rankings.csv")
    secondary_qb_rankings = pd.read_csv("data/secondary_qb_rankings.csv")

    merged_qb_rankings = pd.merge(primary_qb_rankings, secondary_qb_rankings, on='QB')
    merged_qb_rankings['Mean'] = (merged_qb_rankings['Points_x'] + merged_qb_rankings['Points_y'])/2
    merged_qb_rankings = merged_qb_rankings.rename(columns = {
        'Points_x': 'M1_Points',
        'Points_y': 'M2_Points'
    })
    merged_qb_rankings = merged_qb_rankings.sort_values(by='Mean', ascending=False)
    merged_qb_rankings = merged_qb_rankings.drop(columns=['Unnamed: 0_x', 'Unnamed: 0_y'])

    return merged_qb_rankings.to_dict(orient="records")