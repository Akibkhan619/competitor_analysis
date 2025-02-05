import os

import pandas as pd
from modules.swot_analyzer import SWOTAnalyzer


def main():
    # Define paths
    processed_folder = "data/processed"
    input_file = os.path.join(processed_folder, "laptops_data.xlsx")

    # Load data
    df = pd.read_excel(input_file)
    print(f"[SWOT] Loaded data from {input_file}")

    # Initialize SWOT Analyzer with batch support
    swot_analyzer = SWOTAnalyzer(model_name="google/flan-t5-large")  # Adjust batch_size based on memory

    # Generate SWOT analysis for each product
    final_df = swot_analyzer.generate_swot_for_all(df.head(10))

    # Save the updated DataFrame
    output_file = os.path.join(processed_folder, "final_data_with_swot_analyses_1.xlsx")
    final_df.to_excel(output_file, index=False)
    print(f"[Main] Final data with SWOT analyses saved to {output_file}")

if __name__ == "__main__":
    main()
