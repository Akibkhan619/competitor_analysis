import json
import pickle

import pandas as pd
import torch
from sentence_transformers import SentenceTransformer


class LaptopRecommender:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Initialize the Laptop Recommender with a Sentence Transformer model.
        """
        self.model = SentenceTransformer(model_name)

    def generate_embeddings(self, df, text_cols):
        """
        Generate embeddings for selected text columns and store them in the dataframe.
        :param df: DataFrame containing laptop details.
        :param text_cols: List of columns to generate embeddings from.
        :return: DataFrame with an added 'Embedding' column containing list-based text embeddings.
        """
        combined_texts = df[text_cols].astype(str).agg(' '.join, axis=1)
        embeddings = self.model.encode(combined_texts, convert_to_numpy=True)
        df['Embedding'] = embeddings.tolist()
        return df

    def save_embeddings(self, df, embedding_file="data/processed/laptop_embeddings.pkl", config_file="config/recommender_config.json"):
        """
        Save embeddings as a Pickle file and create a JSON config file.
        """
        # Save embeddings as a Pickle file
        with open(embedding_file, "wb") as f:
            pickle.dump(df, f)
        print(f"✅ Embeddings saved to {embedding_file}")

        # Save metadata in a JSON config
        config_data = {
            "embedding_file": embedding_file,
            "query": ""
        }
        with open(config_file, "w") as f:
            json.dump(config_data, f, indent=4)
        print(f"✅ Config saved to {config_file}")
