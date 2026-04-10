import pandas as pd
import numpy as np

# --- 1. Load and Explore ---
df = pd.read_csv("data/trends_clean.csv")

# print basic info
print(f"Loaded data: {df.shape}")
print("First 5 rows:")
print(df.head())

# get averages using pandas first
avg_score = df['score'].mean()
avg_comments = df['num_comments'].mean()

# formatting with :,.0f to add commas and remove decimals like the example
print(f"Average score   : {avg_score:,.0f}")
print(f"Average comments: {avg_comments:,.0f}")

print("\n--- NumPy Stats ---")

# --- 2. Basic Analysis with NumPy ---
# grab the score column as a numpy array
scores = df['score'].values

# calculate stats with numpy
mean_score = np.mean(scores)
median_score = np.median(scores)
std_dev = np.std(scores)
max_score = np.max(scores)
min_score = np.min(scores)

print(f"Mean score   : {mean_score:,.0f}")
print(f"Median score : {median_score:,.0f}")
print(f"Std deviation: {std_dev:,.0f}")
print(f"Max score    : {max_score:,.0f}")
print(f"Min score    : {min_score:,.0f}")

# find the most popular category
cat_counts = df['category'].value_counts()
top_category = cat_counts.index[0]
top_count = cat_counts.iloc[0]
print(f"Most stories in: {top_category} ({top_count} stories)")

# find the story with the absolute most comments
# idxmax() gives the row number of the highest value
max_comment_row = df['num_comments'].idxmax()
top_story_title = df.loc[max_comment_row, 'title']
top_story_comments = df.loc[max_comment_row, 'num_comments']

print(f'Most commented story: "{top_story_title}"  — {top_story_comments:,} comments')


# --- 3. Add New Columns ---
# formula: comments / (score + 1)
df['engagement'] = df['num_comments'] / (df['score'] + 1)

# True if score is bigger than the average, False otherwise
df['is_popular'] = df['score'] > avg_score


# --- 4. Save the Result ---
save_path = "data/trends_analysed.csv"
df.to_csv(save_path, index=False)
print(f"\nSaved to {save_path}")