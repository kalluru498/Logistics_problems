# optimizer.py
import pandas as pd
from typing import List, Dict

def optimize_loading(doors_df: pd.DataFrame, trailer: Dict) -> Dict:
    instructions = []
    total_weight = 0
    total_volume = 0
    x, y, z = 0, 0, 0

    for i, row in doors_df.iterrows():
        weight = row['weight_kg']
        width = row['width_in']
        height = row['height_in']

        orientation = 'upright' if row.get('material', '').lower() in ['glass', 'vinyl'] else 'flat'

        strap = 'Yes' if weight > 40 or row.get('material', '').lower() in ['glass'] else 'No'
        instructions.append(
            f"✅ Place **{row['door_type']}** ({orientation}) at (x={x}, y={y}, z={z}). Strap Required: {strap}"
        )

        total_weight += weight
        total_volume += (width * height)
        x += width  # Move x for next door

        if x > trailer['length_in']:
            x = 0
            y += width

        if y > trailer['width_in']:
            y = 0
            z += height

    summary = {
        "Total Doors": len(doors_df),
        "Used Weight (kg)": round(total_weight, 2),
        "Max Capacity (kg)": trailer['max_weight_kg'],
        "Trailer Dimensions (LxWxH in)": f"{trailer['length_in']}x{trailer['width_in']}x{trailer['height_in']}"
    }

    return {"instructions": instructions, "summary": summary}
