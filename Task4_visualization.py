# task4_visualization.py
# Name: Yash Kadam

import pandas as pd
import matplotlib.pyplot as plt
import os

# -------- Load the data --------
df = pd.read_csv("data/trends_analysed.csv")

# -------- Create outputs folder if not exists --------
if not os.path.exists("outputs"):
    os.makedirs("outputs")


# ===============================
# Chart 1: Top 10 stories by score
# ===============================

# sorting and taking top 10
top10 = df.sort_values("score", ascending=False).head(10)

# shorten long titles (otherwise messy on graph)
top10["title_short"] = top10["title"].apply(
    lambda x: x[:50] + "..." if len(x) > 50 else x
)

plt.figure(figsize=(10, 6))

# horizontal bar chart
plt.barh(top10["title_short"], top10["score"])

plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Stories")

# highest score on top
plt.gca().invert_yaxis()

# saving chart
plt.savefig("outputs/chart1_top_stories.png")
plt.close()


# ===============================
# Chart 2: Stories per category
# ===============================

# count categories
cat_counts = df["category"].value_counts()

plt.figure(figsize=(8, 5))

plt.bar(cat_counts.index, cat_counts.values)

plt.title("Stories per Category")
plt.xlabel("Category")
plt.ylabel("Count")

plt.xticks(rotation=45)

plt.savefig("outputs/chart2_categories.png")
plt.close()


# ===============================
# Chart 3: Score vs Comments
# ===============================

# split data based on popularity
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.figure(figsize=(8, 5))

# plotting both
plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

plt.title("Score vs Comments")
plt.xlabel("Score")
plt.ylabel("Comments")

plt.legend()

plt.savefig("outputs/chart3_scatter.png")
plt.close()


# ===============================
# Bonus: Dashboard
# ===============================

fig, ax = plt.subplots(1, 3, figsize=(18, 5))

# chart 1
ax[0].barh(top10["title_short"], top10["score"])
ax[0].set_title("Top Stories")
ax[0].invert_yaxis()

# chart 2
ax[1].bar(cat_counts.index, cat_counts.values)
ax[1].set_title("Categories")
ax[1].tick_params(axis='x', rotation=45)

# chart 3
ax[2].scatter(popular["score"], popular["num_comments"], label="Popular")
ax[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
ax[2].set_title("Score vs Comments")
ax[2].legend()

# overall title
plt.suptitle("TrendPulse Dashboard")

plt.savefig("outputs/dashboard.png")
plt.close()

print("done")