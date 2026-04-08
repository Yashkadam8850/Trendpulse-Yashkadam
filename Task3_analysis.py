# task3_analysis.py
# Author: Yash Kadam
# Task 3 — Analysis with Pandas & NumPy

import pandas as pd
import numpy as np
import os

# ------------------------------
# Step 1: Load and Explore Data
# ------------------------------

# File path
FILE_PATH = "data/trends_clean.csv"

# Check if file exists
if not os.path.exists(FILE_PATH):
    print(f"Error: File not found -> {FILE_PATH}")
    exit()

# Load CSV into DataFrame
df = pd.read_csv(FILE_PATH)

# Print shape
print(f"\nLoaded data: {df.shape}")

# Print first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Compute averages using Pandas
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {int(avg_score):,}")
print(f"Average comments: {int(avg_comments):,}")


# ---------------------------------
# Step 2: Basic Analysis with NumPy
# ---------------------------------

print("\n--- NumPy Stats ---")

# Convert columns to NumPy arrays
scores = df["score"].to_numpy()
comments = df["num_comments"].to_numpy()

# Mean, Median, Standard Deviation
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

print(f"Mean score   : {int(mean_score):,}")
print(f"Median score : {int(median_score):,}")
print(f"Std deviation: {int(std_score):,}")

# Max and Min score
max_score = np.max(scores)
min_score = np.min(scores)

print(f"Max score    : {max_score:,}")
print(f"Min score    : {min_score:,}")

# Category with most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_count = category_counts.max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")

# Story with most comments
max_comments_index = np.argmax(comments)
top_story = df.iloc[max_comments_index]

print(f'\nMost commented story: "{top_story["title"]}" — {top_story["num_comments"]:,} comments')


# ------------------------------
# Step 3: Add New Columns
# ------------------------------

# Engagement = num_comments / (score + 1)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular = True if score > average score
df["is_popular"] = df["score"] > avg_score


# ------------------------------
# Step 4: Save Result
# ------------------------------

OUTPUT_PATH = "data/trends_analysed.csv"

# Save to CSV
df.to_csv(OUTPUT_PATH, index=False)

print(f"\nSaved to {OUTPUT_PATH}")