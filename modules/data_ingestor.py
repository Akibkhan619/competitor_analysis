# modules/data_ingestor.py
import os
import pandas as pd

class DataIngestor:
    def __init__(self, data_folder):
        self.data_folder = data_folder

    def load_data(self):
        data_frames = []
        for file in os.listdir(self.data_folder):
            if file.endswith(".csv"):
                file_path = os.path.join(self.data_folder, file)
                df = pd.read_csv(file_path)
                data_frames.append(df)
        if data_frames:
            combined_df = pd.concat(data_frames, ignore_index=True)
            print(f"[DataIngestor] Loaded {len(combined_df)} records from CSV files in {self.data_folder}")
            return combined_df
        else:
            print("[DataIngestor] No CSV files found.")
            return pd.DataFrame()
