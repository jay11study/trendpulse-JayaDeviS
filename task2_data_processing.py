import pandas as pd
import os

# Step 1: Load the JSON file
file_location = "data/trends_20260410.json"

# JSON into DataFrame
if not os.path.exists(file_location):
    print("Oops! File not found. Check your file name or folder path.")
else:
    raw_data = pd.read_json(file_location)

raw_data = pd.read_json(file_location)

# Initial count
total_rows = len(raw_data)
print(f"Loaded {total_rows} stories from {file_location}")


# Step 2 - Clean the data
clean_data = raw_data.copy()

# Duplicates
before_dupes = len(clean_data)
clean_data = clean_data.drop_duplicates(subset="post_id")
after_dupes = len(clean_data)

print(f"After removing duplicates: {after_dupes}")

# Missing values
before_nulls = len(clean_data)
clean_data = clean_data.dropna(subset=["post_id", "title", "score"])
after_nulls = len(clean_data)

print(f"After removing nulls: {after_nulls}")

# Data types
clean_data["score"] = clean_data["score"].astype(int)
clean_data["num_comments"] = clean_data["num_comments"].astype(int)

# Low quality
before_filter = len(clean_data)
clean_data = clean_data[clean_data["score"] >= 5]
after_filter = len(clean_data)

print(f"After removing low scores: {after_filter}")

# Whitespace
clean_data["title"] = clean_data["title"].str.strip()


# Step 3: Save cleaned data
output_file = "data/trends_clean.csv"
clean_data.to_csv(output_file, index=False)

final_count = len(clean_data)
print(f"\nSaved {final_count} rows to {output_file}")


# Step 4: Summary (stories per category)
print("\nStories per category:")
category_summary = clean_data["category"].value_counts()

print(category_summary)
