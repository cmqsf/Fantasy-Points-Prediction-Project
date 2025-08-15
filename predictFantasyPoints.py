import pandas as pd
import numpy as np
import random as rd
import logging
import math

from fastapi import FastAPI, HTTPException
import uvicorn
from predictMethods import *

app = FastAPI()
rd.seed(23232301)

# Load data
ff24 = pd.read_csv("data/fantasyFootball2024.csv")
ff23 = pd.read_csv("data/fantasyFootball2023.csv")
ff22 = pd.read_csv("data/fantasyFootball2022.csv")
ff21 = pd.read_csv("data/fantasyFootball2021.csv")

# Clean data
stats = cleanStats([ff24, ff23, ff22, ff21])

@app.get("/predict")
async def getPredictions(player: str): 
    try:  
        player_stats = stats[stats["player"] == player]

        if player_stats.empty:
            raise HTTPException(status_code=404, detail="Player not found")

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

            """
            if player_stats.iloc[0]['fantasy_position'] == 'TE': 
                tes = tightEnds(stats)
                ypred = getPredictedFantasyPoints(tes, player, 170)
            """

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
            'pointsPerWeekAvg': {
                'low': avg_low,
                'high': avg_high,
                'average': round((avg_high+avg_low)/2, 2)
            }
        }

    except HTTPException:
        raise  # let FastAPI handle expected errors
    except Exception as Argument: 
        logging.exception("Prediction failed:")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
