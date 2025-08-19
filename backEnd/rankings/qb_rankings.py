
import pandas as pd
import numpy as np
import random as rd
import logging
import math
import os
import logging
import statistics

from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import HTMLResponse
import uvicorn

from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def router_lifespan(app: APIRouter):
    global stats
    current_dir = os.path.dirname(os.path.abspath(__file__))

    yield

router = APIRouter(lifespan=router_lifespan)

@router.get("/qb-rankings", response_class = HTMLResponse)
def get_qb_rankings():
    primary_qb_rankings = pd.read_csv("data/qb_rankings.csv")
    secondary_qb_rankings = pd.read_csv("data/secondary_qb_rankings.csv")

    merged_qb_rankings = pd.merge(primary_qb_rankings, secondary_qb_rankings, on='QB')
    merged_qb_rankings['Mean'] = (merged_qb_rankings['Points_x'] + merged_qb_rankings['Points_y'])/2
    merged_qb_rankings = merged_qb_rankings.rename(columns = {
        'Points_x': 'Method 1 Points',
        'Points_y': 'Method 2 Points'
    })
    merged_qb_rankings = merged_qb_rankings.sort_values(by='Mean', ascending=False)
    merged_qb_rankings = merged_qb_rankings.drop(columns=['Unnamed: 0_x', 'Unnamed: 0_y'])

    merged_table = merged_qb_rankings.to_html(index=False, classes="merged_qb_rankings", border=0)

    return f"""
    <!DOCTYPE HTML>
    <html>
        <head>
            <title>QB Rankings</title>
        </head>
        <body>
            <h1>QB Rankings</h1>
            {merged_table}
        </body>
    </html>
    """