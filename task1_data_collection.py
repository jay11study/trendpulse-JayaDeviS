import requests
import time
import os
import json
from datetime import datetime

# Step 1 - Make the API Calls
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

headers = {"User-Agent": "TrendPulse/1.0"}

# First 500 story IDs
try:
    response = requests.get(TOP_STORIES_URL, headers=headers)
    story_ids = response.json()[:500]
    print(f"Fetched {len(story_ids)} story IDs successfully.")
except Exception as e:
    print("Failed to fetch top stories:", e) # handling error
    story_ids = []


# Step 2 - Extract the Fields
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

gathered_stories = []

# Loop category by category (important for sleep condition)
for category, keywords in categories.items():

    print(f"\nCollecting stories for category: {category}")
    count = 0

    for story_id in story_ids:

        # Stop on 25 stories
        if count >= 25:
            break

        try:
            res = requests.get(ITEM_URL.format(story_id), headers=headers)
            story = res.json()

            # Skipping the invalid datas
            if story is None or "title" not in story:
                continue

            title = story.get("title", "")
            title_lower = title.lower()

            # Checking if title matches any keyword
            if any(keyword in title_lower for keyword in keywords):

                # Extract required fields
                cleaned_story = {
                    "post_id": story.get("id"),
                    "title": title,
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", "unknown"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                gathered_stories.append(cleaned_story)
                count += 1

        except Exception as e:
            print(f"Error fetching story {story_id}: {e}")
            continue

    print(f"Collected {count} stories for {category}")

    # Waiting for 2 secs
    time.sleep(2)


# Step 3 - Save to JSON File

# Creating a folder if not exist
if not os.path.exists("data"):
    os.makedirs("data")

filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

# Saving data
with open(filename, "w", encoding="utf-8") as file:
    json.dump(gathered_stories, file, indent=4)

# Output
print(f"\nCollected {len(gathered_stories)} stories. Saved to {filename}")
