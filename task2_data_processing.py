import pandas as pd
import glob
import os

# --- 1. Load the JSON File ---
# Let's find the JSON file we created in Task 1. 
# glob helps us find files that match a pattern, so we don't have to hardcode the date.
json_files = glob.glob("data/trends_*.json")

# Make sure we actually found a file
if len(json_files) == 0:
    print("Error: Could not find any JSON file in the data/ folder. Make sure Task 1 ran successfully!")
    exit()

# Grab the first file it finds (should be the one we just made)
my_file = json_files[0] 

# Pandas makes loading json super easy
df = pd.read_json(my_file)
print(f"Loaded {len(df)} stories from {my_file}")

# --- 2. Clean the Data ---

# Issue 1: Duplicates
# The assignment says to remove any rows with the exact same post_id
df = df.drop_duplicates(subset=['post_id'])
print(f"After removing duplicates: {len(df)}")

# Issue 2: Missing values
# Drop rows where post_id, title, or score is missing (null/NaN)
df = df.dropna(subset=['post_id', 'title', 'score'])
print(f"After removing nulls: {len(df)}")

# Issue 3: Low quality
# Keep only the stories where the score is 5 or more
df = df[df['score'] >= 5]
print(f"After removing low scores: {len(df)}")

# Issue 4: Data types
# First, if any story is missing the number of comments, fill it with 0 so the integer conversion doesn't crash
df['num_comments'] = df['num_comments'].fillna(0)

# Now convert score and num_comments to integers like the instructions asked
df['score'] = df['score'].astype(int)
df['num_comments'] = df['num_comments'].astype(int)

# Issue 5: Whitespace
# Strip extra spaces from the beginning and end of the title string
df['title'] = df['title'].str.strip()


# --- 3. Save as CSV ---
csv_filename = "data/trends_clean.csv"

# Save to CSV. We use index=False so Pandas doesn't save an annoying extra column of row numbers
df.to_csv(csv_filename, index=False)
print(f"Saved {len(df)} rows to {csv_filename}")

# Print the final summary of stories per category
print("Stories per category:")

# value_counts() automatically counts how many times each category shows up in the column
category_counts = df['category'].value_counts()

# Loop through the results to print them out nicely
for category_name, count in category_counts.items():
    # I'm using ljust(15) to add spaces so the numbers line up neatly like the example output
    print(f"  {category_name.ljust(15)} {count}")