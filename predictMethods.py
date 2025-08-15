import pandas as pd
import numpy as np
import sklearn as sk
import statistics as math
import random as rd

import logging

rd.seed(23232301)

from sklearn.ensemble import RandomForestRegressor

def cleanStats(partial_stats): 
    
    try:
        if isinstance(partial_stats, list): 
            stats = pd.concat(partial_stats, ignore_index = True)
        else: 
            stats = partial_stats
        
        stats = stats.rename(columns = {
            'Rk': 'rank', 
            'Player': 'player', 
            'Tm': 'team', 
            'Age': 'age',
            'FantPos': 'fantasy_position',
            'G': 'games_played', 
            'GS': 'games_started', 
            'Cmp': 'passes_completed', 
            'Att': 'passes_attempted', 
            'Yds': 'passing_yds',
            'TD': 'passing_tds',
            'Int': 'interceptions',
            'Att.1': 'rushing_attempts', 
            'Yds.1': 'rush_yds', 
            'Y/A': 'rush_yds_per_attempt',
            'TD.1': 'rush_tds',
            'Tgt': 'targets', 
            'Rec': 'receptions', 
            'Yds.2': 'receiving_yds', 
            'Y/R': 'receiving_yds_per_reception',
            'TD.2': 'receiving_tds', 
            'Fmb': 'fumbles', 
            'FL': 'fumbles_lost', 
            'TD.3': 'total_tds', 
            '2PM': '2pt_conversions_made', 
            '2PP': '2pt_conversion_passes',
            'PosRank': 'position_rank', 
            'OvRank': 'overall_rank'
        })
        
        yds = 0.1*(stats['rush_yds'] + stats['receiving_yds']) + 0.04*stats['passing_yds']
        tds = 6*(stats['rush_tds'] + stats['receiving_tds']) + 4*stats['passing_tds']
        recs = 0.5*stats['receptions']
        two = 2*stats['2pt_conversions_made'] + 2*stats['2pt_conversion_passes']
        lost = -2*stats['fumbles'] - 1.5*stats['interceptions'] 
        stats['fantasy_points'] = yds + tds + recs + lost
        
        stats = stats.drop(columns = ['team',
                                    'rank', 
                                    'FantPt', 
                                    'PPR', 
                                    'DKPt', 
                                    'FDPt', 
                                    'VBD',  
                                    '-9999'], axis = 1)
        
        return stats
    
    except Exception as Argument: 
        logging.error(f"cleanStats: {Argument}")

def quarterbacks(stats): 
    
    qbs = stats[stats['fantasy_position'] == "QB"]
    
    qbs = qbs[['player', 
               'age', 
               'games_played', 
               'passes_completed', 
               'passing_yds', 
               'passing_tds', 
               'interceptions', 
               'rushing_attempts', 
               'rush_yds_per_attempt', 
               'total_tds', 
               '2pt_conversion_passes', 
               'fantasy_points']]
    
    qbs = qbs.dropna()
    
    return qbs

def runningBacks(stats):
    
    rbs = stats[stats['fantasy_position'] == "RB"]
    rbs = rbs[[
        'player', 
        'age', 
        'games_started', 
        'rush_yds', 
        'rush_yds_per_attempt', 
        'targets', 
        'receiving_yds', 
        'fumbles_lost', 
        'total_tds', 
        'fantasy_points'
    ]]
    
    rbs = rbs.dropna()
    
    return rbs
    
def wideReceivers(stats):
    
    wrs = stats[stats['fantasy_position'] == "WR"]
    
    wrs = wrs[[
        'player', 
        'age',
        'games_started', 
        'rush_yds', 
        'targets', 
        'receptions', 
        'receiving_yds_per_reception', 
        'fumbles_lost', 
        'total_tds', 
        'fantasy_points'
    ]]
    
    wrs = wrs.dropna()
    
    return wrs

def tightEnds(stats):
    
    tes = stats[stats['fantasy_position'] == "TE"]
    
    tes = tes[[
        'player', 
        'age', 
        'games_started', 
        'rushing_attempts', 
        'rush_yds_per_attempt', 
        'targets', 
        'receiving_yds_per_reception', 
        'fumbles_lost', 
        'total_tds',
        'fantasy_points'
    ]]
    
    tes = tes.dropna()
    
    return tes

def getPredictedFantasyPoints(stats, player, estimators): 

    try:     
        x = stats.drop(columns = ['fantasy_points'])
        y = stats[['fantasy_points', 'player']]
        
        x_test = x[x["player"] == player].drop(columns = ['player'])
        x_train = x[x["player"] != player].drop(columns = ['player'])
        
        y_test = y[y["player"] == player].drop(columns = ['player'])
        y_train = y[y["player"] != player].drop(columns = ['player'])
        
        
        model = RandomForestRegressor(n_estimators=estimators, random_state=42)
        model.fit(x_train, y_train.values.ravel())

        y_pred = model.predict(x_test)
        ypred = [round(y_pred[0], 2), round(y_pred[1], 2)]

        print(f"Prediction range: between {round(y_pred[0], 2)} and {round(y_pred[1], 2)} total points")
        print(f"Prediction average per week: between {round(y_pred[0]/14, 2)} and {round(y_pred[1]/14, 2)} points per week")
        
        return ypred
    
    except Exception as Argument: 
        logging.error(f"getPredictedFantasyPoints: {Argument}")
        