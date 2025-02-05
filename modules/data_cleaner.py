import re
import pandas as pd

# Mapping for Bangla digits to English
BANGLA_DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")

def convert_bangla_numerals(text):
    """Convert Bangla numerals in the text to English digits."""
    if text:
        return text.translate(BANGLA_DIGITS)
    return text

class DataCleaner:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def clean_price(self, price_str):
        """
        Cleans and converts a price string into a numeric value.
        For Startech prices like "125,000৳128,000৳", only the first price is considered.
        """
        if not price_str:
            return None
        # Convert any Bangla numerals to English
        price_str = convert_bangla_numerals(price_str)
        # If there is a currency symbol (৳), split and take the first part.
        if "৳" in price_str:
            price_str = price_str.split("৳")[0]
        # Remove commas and any non-digit (except period) characters.
        price_str = re.sub(r'[^\d.]', '', price_str)
        try:
            return float(price_str)
        except ValueError:
            return None

    def clean_description(self, description):
        """
        Cleans the description by:
          - Converting to a string.
          - Removing HTML tags and extra whitespace.
          - Removing repetitive or promotional leading text.
          - Removing unwanted promotional sentences.
          - Removing sections starting with "Buying Guide" or "Why Choose".
        """
        description = str(description) if description is not None else ""
        # Remove HTML tags.
        description = re.sub(r'<[^>]+>', ' ', description)
        # Normalize whitespace.
        description = re.sub(r'\s+', ' ', description).strip()
        # Remove unwanted introductory lines anywhere in the description:
        # - Lines starting with "Features of ... Laptop In Bangladesh"
        # - Lines starting with "Details Overview for ... Laptop"
        description = re.sub(
            r'(?im)^(Features of .*?Laptop In Bangladesh\s*|Details Overview for .*?Laptop\s*)\n?',
            '',
            description
        )
        # Remove leading "Description" (for Startech).
        description = re.sub(r'^Description\s*', '', description, flags=re.IGNORECASE)
        # Remove promotional sentence (specific fixed text)
        description = re.sub(
            r' Order Online Or Visit your Nearest Star Tech Shop to get yours at lowest price.',
            '',
            description
        )
        # Remove generic promotional sentences that start with "You can buy ..." up to phrases like
        # "from our website" or "visit our showrooms nearby"
        description = re.sub(
            r'(?i)You can buy .*?(from our website or visit our showrooms nearby.)[\.!]*\s*',
            '',
            description
        )
        # Remove generic promotional sentences that start with "Buy ..." up to phrases like
        # "Laptop From Star Tech"
        description = re.sub(
            r'(?i)Buy .*?(Laptop From Star Tech.)[\.!]*\s*',
            '',
            description
        )
        # Remove generic promotional sentences that start with "In Bangladesh, you can get" up to phrases like
        # "Laptop From Star Tech."
        description = re.sub(
            r'(?i)In Bangladesh, you can get .*?(Laptop From Star Tech.)[\.!]*\s*',
            '',
            description
        )
        # Remove any trailing sections starting with "Buying Guide" or "Why Choose".
        description = re.split(r'Buying Guide|Why Choose', description)[0]
        return description

    def clean_data(self):
        # Clean Price: process each record using clean_price
        if 'Price' in self.df.columns:
            self.df['Cleaned_Price'] = self.df['Price'].apply(lambda x: self.clean_price(str(x)))
        else:
            self.df['Cleaned_Price'] = None

        # Clean Technical Details:
        if 'Technical Details' in self.df.columns:
            tech = self.df['Technical Details'].apply(lambda x: re.sub(r'\s+', ' ', str(x)).strip())
            # Remove the unwanted phrases "Quick Overview" and "Key Features"
            tech = tech.apply(lambda x: re.sub(r'(Quick Overview|Key Features)', '', x, flags=re.IGNORECASE))
            # Remove "View More Info" from technical details.
            tech = tech.apply(lambda x: re.sub(r'(?i)View More Info', '', x))
            tech = tech.apply(lambda x: re.sub(r'(?i)Licensed Application - No', '', x))
            self.df['Cleaned_Tech_Details'] = tech
        else:
            self.df['Cleaned_Tech_Details'] = ""

        # Clean Description:
        if 'Description' in self.df.columns:
            self.df['Cleaned_Description'] = self.df['Description'].apply(self.clean_description)
        else:
            self.df['Cleaned_Description'] = ""

        print("[DataCleaner] Data cleaning complete.")
        return self.df
