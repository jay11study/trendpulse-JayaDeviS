import pandas as pd
import numpy as np

# Step 1 - Load and Explore
file_path = "data/trends_clean.csv"

# Load CSV
trend_data = pd.read_csv(file_path)

# Shape
rows, cols = trend_data.shape
print(f"Loaded data: ({rows}, {cols})")

# First 5 rows
print("\nFirst 5 rows:")
print(trend_data.head())

# Average score and comments
avg_score = trend_data["score"].mean()
avg_comments = trend_data["num_comments"].mean()

print(f"\nAverage score   : {int(avg_score)}")
print(f"Average comments: {int(avg_comments)}")


# Step 2 - Basic Analysis with NumPy
print("\n--- NumPy Stats ---")

scores_array = trend_data["score"].values

# Stats
mean_score = np.mean(scores_array)
median_score = np.median(scores_array)
std_score = np.std(scores_array)

max_score = np.max(scores_array)
min_score = np.min(scores_array)

print(f"Mean score   : {int(mean_score)}")
print(f"Median score : {int(median_score)}")
print(f"Std deviation: {int(std_score)}")
print(f"Max score    : {max_score}")
print(f"Min score    : {min_score}")

# Category with most stories
top_category = trend_data["category"].value_counts().idxmax()
top_count = trend_data["category"].value_counts().max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")

# Story has the most comments
max_comment_row = trend_data.loc[trend_data["num_comments"].idxmax()]
top_title = max_comment_row["title"]
top_comments = max_comment_row["num_comments"]

print(f'\nMost commented story: "{top_title}" — {top_comments} comments')


# Step 3 - Add New Columns
#  how much discussion a story gets per upvote
trend_data["engagement"] = trend_data["num_comments"] / (trend_data["score"] + 1)

# Popular >> score greater than average
trend_data["is_popular"] = trend_data["score"] > avg_score


# Step 4 - Save the Result
output_path = "data/trends_analysed.csv"
trend_data.to_csv(output_path, index=False)

print(f"\nSaved to {output_path}")
