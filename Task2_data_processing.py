import pandas as pd
import os
import json

# ---------- Step 1: Load JSON File ----------
file_path = "data/collected_data.json"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    print(f"Error loading file: {e}")

# ----------- Step 2: Convert to DataFrame ----------
df = pd.DataFrame(data)


# ---------- Step 3: Cleaning ----------
# Example: Remove record with epmty title
df = df[df["title"].str.strip() != ""]
print(f"Records after cleaning: {len(df)}")

# -------- Remove duplicates ---------
df = df.drop_duplicates(subset=["post_id"])
print(f"Records after removing duplicates: {len(df)}")

# ------- Remove nulls ---------
df = df.dropna(subset=["title"])
print(f"Records after removing nulls: {len(df)}")

# -------Fix data types --------
df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0).astype(int)
df["num_comments"] =pd.to_numeric(df["num_comments"], errors="coerce").fillna(0).astype(int)
df["collected_at"] = pd.to_datetime(df["collected_at"], errors="coerce")
df["collected_at"] = df["collected_at"].dt.strftime("%Y-%m-%d %H:%M:%S")
print(f"Data types after fixing:\n{df.dtypes}")
print(f"Sample data:\n{df.head()}")
print(f"Total records after cleaning: {len(df)}")
print(f"Unique categories: {df['category'].nunique()}")
print(f"Unique authors: {df['author'].nunique()}")

# ---------- Remove low scores ----------
df = df[df["score"] >= 5]
print(f"Records after removing low scores: {len(df)}")
df = df[df["num_comments"] >= 5]
print(f"Records after removing low comments: {len(df)}")
df = df[df["collected_at"] >= "2024-01-01"]
print(f"Records after removing old records: {len(df)}")

# ------------ Strip whitespace -------------
df["title"] = df["title"].str.strip()
df["author"] = df["author"].str.strip()

# ------------ step 4: Save as CSV -------------
output_path = "data/trends_clean.csv"

try:
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"\nSaved {len(df)} rows to {output_path}")
except Exception as e:
    print(f"Error saving CSV: {e}")

# ----------- Step 5: Summary -----------
print(f"\nFinal Summary:")
print(f"Total records: {len(df)}")
print(f"Unique categories: {df['category'].nunique()}")
print(f"Unique authors: {df['author'].nunique()}")