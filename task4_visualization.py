import pandas as pd
import matplotlib.pyplot as plt
import os

# Setup
file_path = "data/trends_analysed.csv"
viz_data = pd.read_csv(file_path)

# Outputs folder if it doesn't exist
output_folder = "outputs"
os.makedirs(output_folder, exist_ok=True)


# Chart 1 - Top 10 Stories by Score
# Taking top 10 after sorting
top_stories = viz_data.sort_values(by="score", ascending=False).head(10)

# Shorten long titles
top_stories["short_title"] = top_stories["title"].apply(
    lambda x: x[:50] + "..." if len(x) > 50 else x
)

plt.figure(figsize=(10, 6))
plt.barh(top_stories["short_title"], top_stories["score"])
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis()  # highest score on top

plt.tight_layout()
plt.savefig(f"{output_folder}/chart1_top_stories.png")
plt.close()


# Chart 2 - Stories per Category
category_counts = viz_data["category"].value_counts()

plt.figure(figsize=(8, 5))
plt.bar(category_counts.index, category_counts.values)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

plt.tight_layout()
plt.savefig(f"{output_folder}/chart2_categories.png")
plt.close()


# Chart 3 - Score vs Comments
# Separate popular and non-popular
popular = viz_data[viz_data["is_popular"] == True]
not_popular = viz_data[viz_data["is_popular"] == False]

plt.figure(figsize=(8, 5))
plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()

plt.tight_layout()
plt.savefig(f"{output_folder}/chart3_scatter.png")
plt.close()


# Bonus: Dashboard
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Chart 1
axes[0].barh(top_stories["short_title"], top_stories["score"])
axes[0].set_title("Top Stories")
axes[0].invert_yaxis()

# Chart 2
axes[1].bar(category_counts.index, category_counts.values)
axes[1].set_title("Categories")

# Chart 3
axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axes[2].set_title("Score vs Comments")
axes[2].legend()

fig.suptitle("TrendPulse Dashboard")

plt.tight_layout()
plt.savefig(f"{output_folder}/dashboard.png")
plt.close()


print("All charts saved in 'outputs/' folder ✅")
