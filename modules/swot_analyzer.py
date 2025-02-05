import os

import torch  # Needed for GPU support
from tqdm import tqdm
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


class SWOTAnalyzer:
    def __init__(self, model_name="google/flan-t5-large"):
        # Load the model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        # Move model to GPU if available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def generate_swot(self, description: str):
        # Construct the structured prompt
        prompt = (
            f"Product Description: {description}\n\n"
            "Summarize all the information of this laptop concisely in a few sentences."
        )

        # Tokenize input and move to GPU (if available)
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=512).to(self.device)

        try:
            outputs = self.model.generate(
                inputs["input_ids"],
                max_length=200,  # Adjust as needed
                num_return_sequences=1,
                no_repeat_ngram_size=2,
                num_beams=4,
                early_stopping=True
            )
            swot_analysis = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return swot_analysis
        except Exception as e:
            print(f"Error generating SWOT analysis: {e}")
            return None

    def generate_swot_for_all(self, df, desc_col="Cleaned_Description"):
        swot_analyses = []
        for _, row in tqdm(df.iterrows(), total=len(df), desc="Generating SWOT Analyses"):
            description = row.get(desc_col, "")
            swot_analysis = self.generate_swot(description)
            swot_analyses.append(swot_analysis)
        df['SWOT_Analysis'] = swot_analyses
        print("[SWOTAnalyzer] SWOT analysis generation complete.")
        return df


# import os

# from tqdm import tqdm
# from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


# class SWOTAnalyzer:
#     def __init__(self, model_name="google/flan-t5-large"):
#         # Load the model and tokenizer
#         self.tokenizer = AutoTokenizer.from_pretrained(model_name)
#         self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

#     def generate_swot(self, description: str):
#         # Construct the prompt
        
#         prompt = (
#             f"Product Description: {description}\n\n"
#             "Perform a SWOT analysis of the product described above."
#             "Clearly state the Strengths, Weaknesses, Opportunities, and Threats."
#             "Provide key reasons why someone should consider buying or avoiding this product."
#             "Sumarize all the information asked and try to describe in few sentences."
#         )
#         inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
#         try:
#             outputs = self.model.generate(
#                 inputs["input_ids"],
#                 max_length=200,  # Adjust as needed
#                 num_return_sequences=1,
#                 no_repeat_ngram_size=2,
#                 num_beams=4,
#                 early_stopping=True
#             )
#             swot_analysis = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
#             return swot_analysis
#         except Exception as e:
#             print(f"Error generating SWOT analysis: {e}")
#             return None

#     def generate_swot_for_all(self, df, desc_col="Cleaned_Description"):
#         swot_analyses = []
#         for _, row in tqdm(df.iterrows(), total=len(df), desc="Generating SWOT Analyses"):
#             description = row.get(desc_col, "")
#             swot_analysis = self.generate_swot(description)
#             swot_analyses.append(swot_analysis)
#         df['SWOT_Analysis'] = swot_analyses
#         print("[SWOTAnalyzer] SWOT analysis generation complete.")
#         return df
# import os

# import torch
# from tqdm import tqdm
# from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


# class SWOTAnalyzer:
#     def __init__(self, model_name="google/flan-t5-large", batch_size=4):
#         """
#         Initialize the SWOTAnalyzer with batch inference support.
#         :param model_name: The Hugging Face model name.
#         :param batch_size: Number of inputs to process in parallel.
#         """
#         # Load model and tokenizer
#         self.tokenizer = AutoTokenizer.from_pretrained(model_name)
#         self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
#         self.batch_size = batch_size

#         # Use GPU if available
#         self.device = "cuda" if torch.cuda.is_available() else "cpu"
#         self.model.to(self.device)

#     def generate_swot_batch(self, descriptions):
#         """
#         Generates SWOT analysis for a batch of descriptions.
#         :param descriptions: List of product descriptions.
#         :return: List of SWOT analyses.
#         """
#         prompts = [
#             f"Product Description: {desc}\n\n"
#             "Perform a SWOT analysis of the product described above."
#             "Clearly state the Strengths, Weaknesses, Opportunities, and Threats."
#             "Provide key reasons why someone should consider buying or avoiding this product."
#             "Sumarize all the information asked and try to describe in few sentences."
#             for desc in descriptions
#         ]

#         # Tokenize inputs in batch
#         inputs = self.tokenizer(prompts, return_tensors="pt", padding=True, truncation=True, max_length=512).to(self.device)

#         try:
#             # Generate outputs in batch
#             outputs = self.model.generate(
#                 inputs["input_ids"],
#                 max_length=200,
#                 num_beams=5,
#                 no_repeat_ngram_size=2,
#                 early_stopping=True
#             )

#             # Decode and return results
#             return [self.tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

#         except Exception as e:
#             print(f"Error generating SWOT analysis: {e}")
#             return [None] * len(descriptions)

#     def generate_swot_for_all(self, df, desc_col="Cleaned_Description"):
#         """
#         Processes the entire DataFrame using batch inference.
#         :param df: Pandas DataFrame with product descriptions.
#         :param desc_col: Column name for product descriptions.
#         :return: DataFrame with SWOT analysis.
#         """
#         swot_analyses = []

#         # Process descriptions in batches
#         for i in tqdm(range(0, len(df), self.batch_size), desc="Generating SWOT Analyses"):
#             batch_descriptions = df[desc_col].iloc[i:i+self.batch_size].tolist()
#             batch_swot = self.generate_swot_batch(batch_descriptions)
#             swot_analyses.extend(batch_swot)

#         # Add results to DataFrame
#         df['SWOT_Analysis'] = swot_analyses
#         print("[SWOTAnalyzer] SWOT analysis generation complete.")
#         return df
