# task1_data_collection.py
# Author: Yash Kadam

import requests
import time
import json
import os
from datetime import datetime

# -------------------------------
# CONFIGURATION
# -------------------------------

BASE_URL = "https://hacker-news.firebaseio.com/v0"
HEADERS = {"User-Agent": "TrendPulse/1.0"}

MAX_PER_CATEGORY = 25
TOTAL_IDS = 500

CATEGORY_KEYWORDS = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# -------------------------------
# FETCH FUNCTIONS
# -------------------------------

def fetch_json(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# -------------------------------
# MAIN LOGIC
# -------------------------------

def main():

    # Step 1: Fetch top story IDs
    top_ids = fetch_json(f"{BASE_URL}/topstories.json")
    if not top_ids:
        print("Failed to fetch top stories.")
        return

    top_ids = top_ids[:TOTAL_IDS]

    # Step 2: Prepare tracking structures
    category_counts = {cat: 0 for cat in CATEGORY_KEYWORDS}
    collected_data = []

    # Step 3: Process by category
    for category, keywords in CATEGORY_KEYWORDS.items():

        print(f"Processing category: {category}")

        for story_id in top_ids:

            # Stop if category limit reached
            if category_counts[category] >= MAX_PER_CATEGORY:
                break

            # Fetch story details
            story = fetch_json(f"{BASE_URL}/item/{story_id}.json")
            if not story:
                continue

            title = story.get("title", "")
            if not title:
                continue

            title_lower = title.lower()

            # Check keyword match
            if any(keyword in title_lower for keyword in keywords):

                record = {
                    "post_id": story.get("id"),
                    "title": title,
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", "unknown"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                collected_data.append(record)
                category_counts[category] += 1

        # Wait after each category
        time.sleep(2)

    # -------------------------------
    # SAVE DATA
    # -------------------------------

    os.makedirs("data", exist_ok=True)

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(collected_data, f, indent=4)
    except Exception as e:
        print(f"Error saving file: {e}")
        return

    # -------------------------------
    # FINAL OUTPUT
    # -------------------------------

    print(f"\nCollected {len(collected_data)} stories.")
    print(f"Saved to {filename}")


# -------------------------------
# ENTRY POINT
# -------------------------------

if __name__ == "__main__":
    main()