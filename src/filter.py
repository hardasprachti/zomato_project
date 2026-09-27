import pandas as pd

BUDGET_MAP = {
    "low":    (0,    500),
    "medium": (500,  1500),
    "high":   (1500, 99999),
}

def parse_input(location, budget, cuisine, min_rating, extras=""):
    budget = budget.lower().strip()
    cost_min, cost_max = BUDGET_MAP.get(budget, (0, 99999))
    
    # Safely parse min_rating, defaulting to 0.0 if empty or invalid
    try:
        parsed_min_rating = float(min_rating)
    except (ValueError, TypeError):
        parsed_min_rating = 0.0

    return {
        "location":   location.lower().strip() if location else "",
        "cuisine":    cuisine.lower().strip() if cuisine else "",
        "cost_min":   cost_min,
        "cost_max":   cost_max,
        "min_rating": parsed_min_rating,
        "extras":     extras.strip() if extras else "",
        "budget_label": budget if budget in BUDGET_MAP else "any",
    }

def filter_restaurants(df, user_prefs, top_n=10):
    filtered = df[
        df['location'].str.contains(user_prefs['location'], na=False) &
        df['cuisines'].str.contains(user_prefs['cuisine'], na=False) &
        (df['cost'] >= user_prefs['cost_min']) &
        (df['cost'] <= user_prefs['cost_max']) &
        (df['aggregate_rating'] >= user_prefs['min_rating'])
    ]

    # Sort: highest rating first, then most votes
    filtered = filtered.sort_values(
        by=['aggregate_rating', 'votes'], ascending=False
    )

    return filtered.head(top_n).reset_index(drop=True)

def serialize_restaurants(df):
    lines = []
    for i, row in df.iterrows():
        lines.append(
            f"{i+1}. {row['name']} | Location: {row['location']} | "
            f"Cuisine: {row['cuisines']} | Cost: Rs.{row['cost']} for two | "
            f"Rating: {row['aggregate_rating']} | Type: {row['rest_type']}"
        )
    return "\n".join(lines)
