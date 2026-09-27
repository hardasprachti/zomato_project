import pandas as pd
from src.filter import parse_input, filter_restaurants, serialize_restaurants
from src.prompt_builder import SYSTEM_PROMPT, build_user_prompt
from src.llm_client import get_recommendation
from src.output_formatter import display_recommendations

def main():
    print("\n Welcome to the AI Restaurant Recommender!\n")

    location   = input("Enter your location        : ")
    budget     = input("Budget (low/medium/high)   : ")
    cuisine    = input("Preferred cuisine          : ")
    min_rating = input("Minimum rating (e.g. 4.0)  : ")
    extras     = input("Any other preferences      : ")

    print("\nSearching restaurants...")
    try:
        df = pd.read_csv("data/restaurants.csv")
    except FileNotFoundError:
        print("Error: data/restaurants.csv not found. Please run src/ingest.py first.")
        return
        
    user_prefs = parse_input(location, budget, cuisine, min_rating, extras)
    filtered   = filter_restaurants(df, user_prefs)

    if filtered.empty:
        print("No restaurants found matching your criteria. Try broadening your search.")
        return

    print(f"Found {len(filtered)} matching restaurants. Asking AI to rank them...\n")

    restaurant_data = serialize_restaurants(filtered)
    user_prompt     = build_user_prompt(user_prefs, restaurant_data)
    
    try:
        response = get_recommendation(SYSTEM_PROMPT, user_prompt)
        display_recommendations(response)
    except Exception as e:
        print(f"\nAn error occurred while calling the LLM: {e}")
        print("Please check your .env file and ensure your API keys are valid.")

if __name__ == "__main__":
    main()
