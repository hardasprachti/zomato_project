def display_recommendations(llm_response):
    print("\n" + "="*60)
    print("   TOP RESTAURANT RECOMMENDATIONS FOR YOU")
    print("="*60)
    try:
        print(llm_response)
    except UnicodeEncodeError:
        # Fallback for Windows consoles that don't support UTF-8 characters (like emojis)
        print(llm_response.encode('ascii', errors='replace').decode('ascii'))
    print("="*60 + "\n")
