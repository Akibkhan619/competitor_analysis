import os
import time

import google.generativeai as genai
import pandas as pd
from tqdm import tqdm


class SWOTAnalyzer:
    def __init__(self, model_name="gemini-1.5-flash", api_key="MY_API_KEY"):
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate_swot(self, tech_details: str, description: str):
        # Construct the prompt
        prompt = (
            f"Perform a detailed SWOT analysis for the following laptop product.\n\n"
            f"**Technical Details:** {tech_details}\n"
            f"**Product Description:** {description}\n\n"
            f"Provide the SWOT analysis in the following structured format:\n\n"
            f"**Strengths:** <List key advantages>\n"
            f"**Weaknesses:** <List key drawbacks>\n"
            f"**Opportunities:** <Potential improvements or market trends>\n"
            f"**Threats:** <Potential risks or competition>\n\n"
            f"Keep the response concise and structured."
        )

        try:
            # Call Gemini API
            response = self.model.generate_content(prompt)
            print(response)
            return response.text.strip() if response.text else "Error: No response from API"
        except Exception as e:
            print(f"Error generating SWOT analysis: {e}")
            return "Error: API Call Failed"

    def generate_swot_for_all(self, df, tech_col="Cleaned_Tech_Details", desc_col="Cleaned_Description", delay=3):
        swot_analyses = []
        for _, row in tqdm(df.iterrows(), total=len(df), desc="Generating SWOT Analyses"):
            tech_details = row.get(tech_col, "")
            description = row.get(desc_col, "")
            swot_analysis = self.generate_swot(tech_details, description)
            swot_analyses.append(swot_analysis)
            time.sleep(delay)  # Delay between requests to respect rate limits
        df['SWOT_Analysis'] = swot_analyses
        print("[SWOTAnalyzer] SWOT analysis generation complete.")
        return df

# Usage example
if __name__ == "__main__":
    input_file = "data/processed/laptops_data.xlsx"
    df = pd.read_excel(input_file)

    swot_analyzer = SWOTAnalyzer()
    updated_df = swot_analyzer.generate_swot_for_all(df)

    output_file = "outputs/laptops_swot_output.xlsx"
    updated_df.to_excel(output_file, index=False)
    print(f"SWOT Analysis saved to {output_file}")
