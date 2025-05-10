import pandas as pd

# Load the product CSV
products = pd.read_csv('data/product_recommendation_data.csv')

# Print the column names
print(products.columns)
