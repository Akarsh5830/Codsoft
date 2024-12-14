import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.impute import SimpleImputer

# Sample user-item ratings matrix
data = {
    'User': ['User1', 'User2', 'User3', 'User4', 'User5'],
    'Item1': [5, 4, np.nan, 1, np.nan],
    'Item2': [4, np.nan, 3, 1, 2],
    'Item3': [np.nan, 3, 4, 1, 2],
    'Item4': [1, 2, 2, 5, 4],
}

# Convert to a DataFrame
df = pd.DataFrame(data)
df.set_index('User', inplace=True)
print("Original Ratings Matrix:\n", df)

# Fill missing values (e.g., using mean)
imputer = SimpleImputer(strategy="mean")
filled_ratings = imputer.fit_transform(df)
filled_df = pd.DataFrame(filled_ratings, columns=df.columns, index=df.index)
print("\nFilled Ratings Matrix:\n", filled_df)

# Calculate similarity (user-user collaborative filtering)
similarity_matrix = cosine_similarity(filled_ratings)
similarity_df = pd.DataFrame(similarity_matrix, index=df.index, columns=df.index)
print("\nUser Similarity Matrix:\n", similarity_df)

# Recommend items to a specific user (e.g., User1)
target_user = 'User1'
similar_users = similarity_df[target_user].sort_values(ascending=False)[1:]  # Exclude self
recommended_items = {}

# Aggregate ratings for missing items from similar users
for item in df.columns:
    if np.isnan(df.loc[target_user, item]):  # Item not rated by target user
        weighted_sum = 0
        similarity_sum = 0
        for sim_user, similarity in similar_users.items():
            if not np.isnan(df.loc[sim_user, item]):
                weighted_sum += similarity * df.loc[sim_user, item]
                similarity_sum += similarity
        if similarity_sum > 0:
            recommended_items[item] = weighted_sum / similarity_sum

# Display recommendations
print("\nRecommended Items for {}:\n{}".format(target_user, recommended_items))
