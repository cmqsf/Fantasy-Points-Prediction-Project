
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
                'avg_games_played': player_stats['games_played'].mean(),
                'avg_games_started': player_stats['games_started'].mean(),
                'avg_ints': player_stats['interceptions'].mean(),
                'avg_passing_yds': player_stats['passing_yds'].mean(),
                'avg_rush_yds': player_stats['rush_yds'].mean(),
                'avg_receiving_yds': player_stats['receiving_yds'].mean(), 
                'avg_fumbles': player_stats['fumbles'].mean(),
                'avg_total_tds': player_stats['total_tds'].mean(),
                'avg_overall_rank': player_stats['overall_rank'].mean()
            }
        }
        
    except HTTPException:
        raise  # let FastAPI handle expected errors
    except Exception as Argument: 
        logging.exception(f"Prediction failed: {Argument}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
