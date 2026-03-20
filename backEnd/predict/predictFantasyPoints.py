
import pandas as pd
import numpy as np
import random as rd
import logging
import math
import os
import logging
import statistics

from fastapi import FastAPI, HTTPException, APIRouter
import uvicorn
from predict.predictMethods import *

from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def router_lifespan(app: APIRouter):
    global stats
    current_dir = os.path.dirname(os.path.abspath(__file__))

    yield

router = APIRouter(lifespan=router_lifespan)

# Load data
ff24 = pd.read_csv("data/fantasyFootball2024.csv")
ff23 = pd.read_csv("data/fantasyFootball2023.csv")
ff22 = pd.read_csv("data/fantasyFootball2022.csv")
ff21 = pd.read_csv("data/fantasyFootball2021.csv")

# Clean data
stats = cleanStats([ff24, ff23, ff22, ff21])

def safe_mean(series):
    val = series.mean()
    if val is None or np.isnan(val):
        return None
    return round(val, 2)

@router.get("/predict")
async def getPredictions(player: str): 
    try:  
        if stats is None: 
            raise HTTPException(status_code=404, detail="Not found")
        
        player_stats = stats[stats["player"] == player]

        if player_stats.empty:
            raise HTTPException(status_code=404, detail=f"Player not found")

        else:
            if player_stats.iloc[0]['fantasy_position'] == 'QB': 
                qbs = quarterbacks(stats)
                ypred = getPredictedFantasyPoints(qbs, player, 155)

            if player_stats.iloc[0]['fantasy_position'] == 'RB': 
                rbs = runningBacks(stats)
                ypred = getPredictedFantasyPoints(rbs, player, 290)

            if player_stats.iloc[0]['fantasy_position'] == 'WR': 
                wrs = wideReceivers(stats)
                ypred = getPredictedFantasyPoints(wrs, player, 120)

            if player_stats.iloc[0]['fantasy_position'] == 'TE': 
                tes = tightEnds(stats)
                ypred = getPredictedFantasyPoints(tes, player, 170)
            
            if ypred is None: 
                raise HTTPException(status_code=404, detail="Prediction failed")
            else:
                total_low = round(min(ypred), 2)
                total_high = round(max(ypred), 2)
                avg_low = round(total_low/14, 2)
                avg_high = round(total_high/14, 2)

        return {
            'totalPoints': {
                'low': total_low, 
                'high': total_high,
                'average': round((total_high+total_low)/2, 2)
            },
            'pointsPerWeek': {
                'low': avg_low,
                'high': avg_high,
                'average': round((avg_high+avg_low)/2, 2)
            },
            'playerStats': {
                'player': player, 
                'position': player_stats.iloc[0]['fantasy_position'],
                'avg_games_played': safe_mean(player_stats['games_played']),
                'avg_games_started': safe_mean(player_stats['games_started']),
                'avg_ints': safe_mean(player_stats['interceptions']),
                'avg_passing_yds': safe_mean(player_stats['passing_yds']),
                'avg_rush_yds': safe_mean(player_stats['rush_yds']),
                'avg_receiving_yds': safe_mean(player_stats['receiving_yds']), 
                'avg_fumbles': safe_mean(player_stats['fumbles']),
                'avg_total_tds': safe_mean(player_stats['total_tds']),
                'avg_overall_rank': safe_mean(player_stats['overall_rank'])
            }
        }
        
    except HTTPException:
        raise  # let FastAPI handle expected errors
    except Exception as Argument: 
        logging.exception(f"Prediction failed: {Argument}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
