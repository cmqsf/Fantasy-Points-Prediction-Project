
import pandas as pd
import numpy as np
import random as rd
import logging
import math
import os
import logging
import statistics

from fastapi import FastAPI, HTTPException, APIRouter, Query
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

def generate_rb_rankings():

    primary_rb_rankings = pd.read_csv('data/rb_rankings.csv')
    secondary_rb_rankings = pd.read_csv('data/secondary_rb_rankings.csv')

    merged_rb_rankings = pd.merge(primary_rb_rankings, secondary_rb_rankings, on="RB")
    merged_rb_rankings['Mean'] = round((merged_rb_rankings['Points_x'] + merged_rb_rankings['Points_y'])/2, 2)
    merged_rb_rankings = merged_rb_rankings.rename(columns = {
        'Points_x': 'M1_Points',
        'Points_y': 'M2_Points'
    })

    merged_rb_rankings = merged_rb_rankings.sort_values(by="Mean", ascending=False)
    merged_rb_rankings = merged_rb_rankings.drop(columns=['Unnamed: 0_x', 'Unnamed: 0_y'])
    merged_rb_rankings["drafted"] = False
    merged_rb_rankings.to_csv("data/merged_rb_rankings.csv")

generate_rb_rankings()

@router.get("/rb-rankings", response_class=JSONResponse)
def get_qb_rankings(): 
    merged = pd.read_csv("data/merged_rb_rankings.csv")
    return merged.to_dict(orient="records")




