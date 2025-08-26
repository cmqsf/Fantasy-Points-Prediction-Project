import pandas as pd
import logging

logger = logging.getLogger(__name__)

def generate_rankings(position):

    try:

        primary_rankings = pd.read_csv(f'data/{position.lower()}_rankings.csv')
        secondary_rankings = pd.read_csv(f'data/secondary_{position.lower()}_rankings.csv')

        merged_rankings = pd.merge(primary_rankings, secondary_rankings, on=position)
        merged_rankings['Mean'] = round((merged_rankings['Points_x'] + merged_rankings['Points_y'])/2, 2)
        merged_rankings = merged_rankings.rename(columns = {
            'Points_x': 'M1_Points',
            'Points_y': 'M2_Points'
        })

        merged_rankings = merged_rankings.sort_values(by="Mean", ascending=False)
        merged_rankings = merged_rankings.drop(columns=['Unnamed: 0_x', 'Unnamed: 0_y'])
        merged_rankings["drafted"] = False
        merged_rankings.to_csv(f"data/merged_{position.lower()}_rankings.csv")

    except Exception as e: 
        logger.error(f"Error in generate_rankings: {e}")

generate_rankings('QB')
generate_rankings('RB')
generate_rankings('WR')
generate_rankings('TE')