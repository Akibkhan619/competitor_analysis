import os

import pandas as pd
from modules.laptop_recommender import LaptopRecommender


def main():
    # Load the dataset (250 laptops)
    input_file = "data/processed/feature_extracted.xlsx"
    df = pd.read_excel(input_file)

    # Initialize recommender and generate embeddings
    recommender = LaptopRecommender()
    df = recommender.generate_embeddings(df, text_cols=["Product Name", "Cleaned_Tech_Details", "Cleaned_Description"])


    embedding_file_name = "data/processed/all_laptop_embeddings.pkl"
    # Save embeddings as Pickle and metadata as JSON
    recommender.save_embeddings(df, embedding_file = embedding_file_name)

if __name__ == "__main__":
    main()
