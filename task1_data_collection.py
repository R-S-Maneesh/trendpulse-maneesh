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
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

def main():
    print("Fetching top 500 story IDs from HackerNews...")
    try:
        response = requests.get(BASE_URL_TOP, headers=HEADERS)
        response.raise_for_status()
        top_ids = response.json()[:500] # Grab only the first 500
    except Exception as e:
        print(f"Error fetching top stories: {e}")
        return                      # Exit if we can't even get the IDs

    collected_stories = []
    
    # We will temporarily store fetched stories here so we don't request the same ID twice from the API
    fetched_cache = {} 
    
    # We will track IDs we've already categorized so one story doesn't end up in two categories
    used_ids = set() 

    # --- Category Loop ---
    for category_name, keywords in CATEGORIES.items():
        print(f"Searching for '{category_name}' stories...")
        category_count = 0

        # Look through our 500 IDs to find matches for the current category
        for story_id in top_ids:
            # Stop if we hit the limit for this specific category
            if category_count >= 25:
                break
                
            # Skip if we already assigned this story to another category
            if story_id in used_ids:
                continue

            # Fetch the story details if we haven't seen it yet
            if story_id not in fetched_cache:
                try:
                    item_url = BASE_URL_ITEM.format(story_id)
                    item_res = requests.get(item_url, headers=HEADERS)
                    item_res.raise_for_status()
                    fetched_cache[story_id] = item_res.json()
                except Exception as e:
                    print(f"Failed to fetch story {story_id}: {e}")
                    continue                # Move on to the next ID without crashing

            story_data = fetched_cache[story_id]

            # Some IDs might be comments or polls, we only want actual stories with titles
            if not story_data or 'title' not in story_data:
                continue

            # Case-insensitive check: Convert title to lowercase
            title_lower = story_data['title'].lower()

            # Check if any keyword exists in the title
            if any(keyword in title_lower for keyword in keywords):
                # We found a match! Extract the required fields safely using .get()
                clean_story = {
                    "post_id": story_data.get("id"),
                    "title": story_data.get("title"),
                    "category": category_name,
                    "score": story_data.get("score", 0),
                    "num_comments": story_data.get("descendants", 0),
                    "author": story_data.get("by", "Unknown"),
                    "collected_at": datetime.now().isoformat()
                }
                
                collected_stories.append(clean_story)
                used_ids.add(story_id)
                category_count += 1

        # Requirement: Wait 2 seconds between each category - one sleep per category loop
        time.sleep(2) 

    # --- Save to JSON ---
    # Create 'data' folder if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")

    # Generate filename with today's date (e.g., trends_20240115.json)
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{date_str}.json"

    # Write the list of dictionaries to a JSON file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_stories, f, indent=4)

    print(f"\nCollected {len(collected_stories)} stories. Saved to {filename}")

if __name__ == "__main__":
    main()