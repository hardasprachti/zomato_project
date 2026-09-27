import pandas as pd
from datasets import load_dataset

def load_raw_dataset():
    dataset = load_dataset("ManikaSaini/zomato-restaurant-recommendation", split="train")
    df = dataset.to_pandas()
    return df

def preprocess(df):
    # Select relevant columns
    df = df[['name', 'location', 'cuisines', 'approx_cost(for two people)',
             'rate', 'votes', 'rest_type']].copy()

    # Rename for ease of use
    df.rename(columns={
        'approx_cost(for two people)': 'cost',
        'rate': 'aggregate_rating'
    }, inplace=True)

    # Clean cost column (remove commas, cast to int)
    df['cost'] = df['cost'].astype(str).str.replace(',', '').str.strip()
    df['cost'] = pd.to_numeric(df['cost'], errors='coerce').fillna(0).astype(int)

    # Normalize text columns
    df['location']  = df['location'].str.lower().str.strip()
    df['cuisines']  = df['cuisines'].str.lower().str.strip()
    df['rest_type'] = df['rest_type'].str.lower().str.strip()

    # Clean and handle missing ratings
    df['aggregate_rating'] = df['aggregate_rating'].astype(str).str.replace('/5', '').str.strip()
    df['aggregate_rating'] = pd.to_numeric(df['aggregate_rating'], errors='coerce').fillna(0.0)
    df['votes'] = pd.to_numeric(df['votes'], errors='coerce').fillna(0).astype(int)

    # Drop rows with no name or location
    df.dropna(subset=['name', 'location'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df

def save_csv(df, path="data/restaurants.csv"):
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} restaurants to {path}")

if __name__ == "__main__":
    df = load_raw_dataset()
    df = preprocess(df)
    save_csv(df)
