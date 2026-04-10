import pandas as pd
import matplotlib.pyplot as plt
import os

# --- 1. Setup ---
# create outputs folder if missing
if not os.path.exists("outputs"):
    os.makedirs("outputs")

# load the processed data from task 3
df = pd.read_csv("data/trends_analysed.csv")


# --- 2. Chart 1: Top 10 Stories by Score ---
# get top 10 and make a copy so we don't mess up the main dataframe
top_10 = df.nlargest(10, 'score').copy()

# shorten titles longer than 50 chars
def shorten_title(title):
    if len(title) > 50:
        return title[:47] + "..."
    return title

top_10['short_title'] = top_10['title'].apply(shorten_title)

# flip it so the biggest bar is at the top
top_10 = top_10.iloc[::-1]

plt.figure(figsize=(10, 6))
plt.barh(top_10['short_title'], top_10['score'], color='#4C72B0')
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")
plt.tight_layout() # keeps labels from getting cut off
plt.savefig("outputs/chart1_top_stories.png")
plt.clf() # clear the figure for the next chart


# --- 3. Chart 2: Stories per Category ---
category_counts = df['category'].value_counts()
# list of colors for the bars
colors = ['#55A868', '#C44E52', '#8172B2', '#CCB974', '#64B5CD', 'gray']

plt.figure(figsize=(8, 6))
# plot the bars using our colors
plt.bar(category_counts.index, category_counts.values, color=colors[:len(category_counts)])
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")
plt.xticks(rotation=45) # tilt labels so they fit
plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")
plt.clf()


# --- 4. Chart 3: Score vs Comments ---
plt.figure(figsize=(8, 6))

# split data into popular and non-popular
popular = df[df['is_popular'] == True]
regular = df[df['is_popular'] == False]

# plot regular stories first (gray dots)
plt.scatter(regular['score'], regular['num_comments'], color='gray', alpha=0.6, label='Normal')
# plot popular stories on top (orange dots)
plt.scatter(popular['score'], popular['num_comments'], color='orange', alpha=0.8, label='Popular')

plt.xlabel("Score")
plt.ylabel("Comments")
plt.title("Score vs Comments (Popularity)")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")
plt.clf()


# --- 5. Bonus: Dashboard ---
# create a 2x2 grid for our 3 charts
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("TrendPulse Dashboard", fontsize=16, fontweight='bold')

# Top-Left: Top 10 Stories
axes[0, 0].barh(top_10['short_title'], top_10['score'], color='#4C72B0')
axes[0, 0].set_title("Top 10 Stories by Score")
axes[0, 0].set_xlabel("Score")

# Top-Right: Categories
axes[0, 1].bar(category_counts.index, category_counts.values, color=colors[:len(category_counts)])
axes[0, 1].set_title("Stories per Category")
axes[0, 1].tick_params(axis='x', rotation=45)

# Bottom-Left: Scatter
axes[1, 0].scatter(regular['score'], regular['num_comments'], color='gray', alpha=0.6, label='Normal')
axes[1, 0].scatter(popular['score'], popular['num_comments'], color='orange', alpha=0.8, label='Popular')
axes[1, 0].set_title("Score vs Comments")
axes[1, 0].set_xlabel("Score")
axes[1, 0].set_ylabel("Comments")
axes[1, 0].legend()

# Bottom-Right: Empty (Hide it since we only have 3 charts)
axes[1, 1].axis('off')

plt.tight_layout()
plt.savefig("outputs/dashboard.png")
print("All charts and dashboard generated successfully in the outputs/ folder!")