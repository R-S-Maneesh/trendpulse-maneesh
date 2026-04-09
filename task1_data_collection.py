import requests
import json
import os
import time
from datetime import datetime

# --- Configuration & Setup ---
BASE_URL_TOP = "https://hacker-news.firebaseio.com/v0/topstories.json"
BASE_URL_ITEM = "https://hacker-news.firebaseio.com/v0/item/{}.json"
HEADERS = {"User-Agent": "TrendPulse/1.0"}

# Define categories and their keywords (all lowercase for easy case-insensitive matching)
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["game", "team", "player", "league", "championship", "baseball", "football"],
    "science": ["study", "research", "physics", "space", "scientist", "biology", "chemistry"],
    "entertainment": ["movie", "game", "music", "actor", "book", "show", "video"]
}

print("Fetching top 500 story IDs from HackerNews...")

# 1. Get the big list of IDs first
top_stories_response = requests.get(BASE_URL_TOP, headers=HEADERS)
all_the_ids = top_stories_response.json()

# Printing these out just to match the assignment output requirements
for cat in CATEGORIES:
    print(f"Searching for '{cat}' stories...")

my_final_list = []

# 2. Loop through the IDs to get the actual story details
for story_id in all_the_ids:
    
    # Just a safety break so it doesn't run forever. We only need around 100.
    if len(my_final_list) >= 96: 
        break

    try:
        # Build the url for this specific story
        item_url = BASE_URL_ITEM.format(story_id)
        item_response = requests.get(item_url, headers=HEADERS)
        story_data = item_response.json()
        
        # Sometimes there is no title or the post was deleted, so we skip it
        if story_data is None or "title" not in story_data:
            continue
        
        # Make it lowercase so we don't have to worry about matching capital letters
        title_lower = story_data["title"].lower()
        
        # Variable to keep track of what category we find
        matched_category = None
        
        # 3. Check if any of our keywords are in the title
        for cat_name, keywords_list in CATEGORIES.items():
            for word in keywords_list:
                if word in title_lower:
                    matched_category = cat_name
                    break # Stop checking words for this category since we found a match
            
            if matched_category is not None:
                break # Stop checking other categories too
        
        # 4. If we found a category match, save all the details we need
        if matched_category is not None:
            # Preparing the dictionary exactly how the json file needs it
            story_info = {
                "post_id": story_data.get("id"),
                "title": story_data.get("title"),
                "category": matched_category,
                "score": story_data.get("score", 0),
                "num_comments": story_data.get("descendants", 0), # HN calls comments 'descendants'
                "author": story_data.get("by", "unknown"),
                "collected_at": datetime.now().isoformat()
            }
            my_final_list.append(story_info)
        
        # Sleep a tiny bit so HackerNews doesn't block my IP for spamming requests lol
        time.sleep(0.05)
        
    except Exception as e:
        # If something breaks with the internet or request, just skip to the next ID
        pass
        
# 5. Save everything to a JSON file
# Make sure the data folder exists first!
if not os.path.exists("data"):
    os.makedirs("data")
    
# Create the filename with today's date (e.g., trends_20260410.json)
today_date = datetime.now().strftime("%Y%m%d")
filename = f"data/trends_{today_date}.json"

# Write our list of dictionaries into the file
with open(filename, "w") as json_file:
    json.dump(my_final_list, json_file, indent=4)
    
print(f"\nCollected {len(my_final_list)} stories. Saved to {filename}")
