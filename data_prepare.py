import os

import pandas as pd
from modules.data_cleaner import DataCleaner
from modules.data_ingestor import DataIngestor
from modules.feature_extractor import FeatureExtractor
from tqdm import tqdm


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def main():
    # 1. Data Ingestion from CSV files in data/raw
    data_folder = "data/raw"
    ingestor = DataIngestor(data_folder)
    raw_df = ingestor.load_data()

    # 2. Data Cleaning & Normalization
    cleaner = DataCleaner(raw_df)
    cleaned_df = cleaner.clean_data()
    
    # Save the cleaned data for observation.
    processed_folder = "data/processed"
    ensure_dir(processed_folder)
    cleaned_excel_file = os.path.join(processed_folder, "combined_data_cleaned.xlsx")
    cleaned_df.to_excel(cleaned_excel_file, index=False)
    print(f"[Main] Cleaned data saved to {cleaned_excel_file}")
    
    # 3. Feature Extraction using LLM-based Entity Extraction
    extractor = FeatureExtractor(cleaned_df)
    featured_df = extractor.extract_features()
    
    feature_extracted_excel = os.path.join(processed_folder, "feature_extracted.xlsx")
    featured_df.to_excel(feature_extracted_excel, index=False)
    print(f"[Main] Feature extracted data saved to {feature_extracted_excel}")

if __name__ == "__main__":
    main()
