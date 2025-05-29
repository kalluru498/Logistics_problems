# utils.py
import pandas as pd

def recommend_trailer(doors_df: pd.DataFrame, trailer_df: pd.DataFrame) -> dict:
    total_weight = doors_df['weight_kg'].sum()
    total_area = (doors_df['width_in'] * doors_df['height_in']).sum()

    trailer_df['score'] = trailer_df.apply(
        lambda row: 0 if row['max_weight_kg'] < total_weight else (row['length_in'] * row['width_in'] * row['height_in']), axis=1
    )

    best_trailer = trailer_df.sort_values(by='score', ascending=False).iloc[0]
    return best_trailer.to_dict()
