SYSTEM_PROMPT = """
You are an expert restaurant recommendation assistant.
Your job is to analyze a list of restaurants and the user preferences,
then recommend the top 3-5 restaurants with clear, friendly explanations
for why each one is a great match. Be specific and helpful.
"""

def build_user_prompt(user_prefs, restaurant_data):
    cost_range = f"Rs.{user_prefs['cost_min']}–Rs.{user_prefs['cost_max']}"
    return f"""
User Preferences:
- Location     : {user_prefs['location']}
- Budget       : {user_prefs['budget_label']} (approx. {cost_range} for two)
- Cuisine      : {user_prefs['cuisine']}
- Min Rating   : {user_prefs['min_rating']}
- Other        : {user_prefs.get('extras', 'None')}

Here are the top matching restaurants from our database:

{restaurant_data}

Please rank the top 3-5 restaurants from this list and explain
why each one is a great fit for the user. Format your response as:

1. **Restaurant Name**
   - Cuisine: ...
   - Rating: ...
   - Cost: ...
   - Why this?: ...
"""
