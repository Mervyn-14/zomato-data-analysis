import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

df = pd.read_csv("zomato.csv", encoding='latin-1')
df_clean = df.copy()
df_clean['rate'] = df_clean['rate'].astype(str).str.replace('/5', '', regex=False)
df_clean['rate'] = df_clean['rate'].replace(['NEW', '-', 'nan'], None)
df_clean['rate'] = pd.to_numeric(df_clean['rate'], errors='coerce')


df_clean['votes'] = pd.to_numeric(df_clean['votes'], errors='coerce')

df_clean['approx_cost(for two people)'] = (
    df_clean['approx_cost(for two people)']
    .astype(str)
    .str.replace(',', '', regex=False)
    .replace('nan', None)
)
df_clean['approx_cost(for two people)'] = pd.to_numeric(
    df_clean['approx_cost(for two people)'], errors='coerce'
)

df_clean.dropna(subset=['name', 'location', 'rate', 'cuisines'], inplace=True)


df_clean.reset_index(drop=True, inplace=True)


print("Cleaned Data Summary:")
print(df_clean.info())
print(df_clean.describe())


sns.set(style="whitegrid", palette="pastel", font_scale=1.1)
plt.rcParams["figure.figsize"] = (10, 6)


top_locations = df_clean['location'].value_counts().head(10)
sns.barplot(x=top_locations.values, y=top_locations.index)
plt.title("Top 10 Locations with Most Restaurants")
plt.xlabel("Number of Restaurants")
plt.ylabel("Location")
plt.tight_layout()
plt.show()


cuisine_series = df_clean['cuisines'].dropna().apply(lambda x: [c.strip() for c in x.split(',')])
cuisine_counter = Counter()
for cuisines in cuisine_series:
    cuisine_counter.update(cuisines)
top_cuisines = cuisine_counter.most_common(10)
cuisine_names, cuisine_counts = zip(*top_cuisines)
sns.barplot(x=list(cuisine_counts), y=list(cuisine_names))
plt.title("Top 10 Most Popular Cuisines")
plt.xlabel("Frequency")
plt.ylabel("Cuisine")
plt.tight_layout()
plt.show()


sns.countplot(data=df_clean, x='online_order')
plt.title("Online Ordering Availability")
plt.xlabel("Online Order")
plt.ylabel("Number of Restaurants")
plt.tight_layout()
plt.show()

sns.histplot(df_clean['rate'], bins=20, kde=True)
plt.title("Restaurant Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()
