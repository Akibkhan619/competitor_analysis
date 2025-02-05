import json
import pickle

import pandas as pd
import torch
from sentence_transformers import SentenceTransformer


class QueryProcessor:
    def __init__(self, model_name="all-MiniLM-L6-v2", config_path="config/recommender_config.json", top_k=3):
        """
        Initialize the query processor for laptop recommendations.
        """
        self.model = SentenceTransformer(model_name)
        self.config_path = config_path
        self.top_k = top_k

        # Load Config File
        with open(config_path, "r") as f:
            self.config = json.load(f)

        # Load Embeddings from Pickle File
        with open(self.config["embedding_file"], "rb") as f:
            self.df = pickle.load(f)

        # Convert stored embeddings back to tensors
        self.df['Embedding'] = self.df['Embedding'].apply(lambda x: torch.tensor(x))

    def get_similar_laptops(self, query):
        """
        Find the most similar laptops based on a user query.
        """
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        stored_embeddings = torch.stack(self.df['Embedding'].tolist())

        # Compute cosine similarity
        similarities = torch.nn.functional.cosine_similarity(query_embedding, stored_embeddings, dim=1)

        # Get top K recommendations
        top_indices = similarities.argsort(descending=True)[:self.top_k].tolist()
        return self.df.iloc[top_indices]

    def generate_recommendation_report(self, output_file="outputs/recommendation_report.txt"):
        """
        Generate a structured recommendation report and save it to a text file.
        """
        query = self.config.get("query", "")
        if not query:
            print("⚠️ No query found in config file. Please add a query.")
            return

        top_laptops = self.get_similar_laptops(query)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("📌 Laptop Recommendation Report\n")
            f.write("="*50 + "\n")
            f.write(f"🔍 **Query:** {query}\n\n")
            f.write("🎯 **Top Recommended Laptops:**\n\n")

            for i, (_, row) in enumerate(top_laptops.iterrows(), 1):
                f.write(f"{i}. **{row['Product Name']}**\n")
                f.write(f"   - **Price:** {row.get('Cleaned_Price', 'N/A')} BDT\n")
                f.write(f"   - **Tech Details:** {row['Cleaned_Tech_Details']}\n")
                f.write(f"   - **Description:** {row['Cleaned_Description']}\n")
                f.write(f"   - **Product Link:** {row['URL']}\n")
                f.write("="*50 + "\n")

        print(f"✅ Recommendation report saved to {output_file}")
