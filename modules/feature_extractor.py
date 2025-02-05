import re
import pandas as pd
from tqdm import tqdm

class FeatureExtractor:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
    
    def extract_processor(self, text: str):
        text = str(text)
        # For Ryans format: if "Processor Type" exists, capture text between "Processor Type" and "RAM"
        if "Processor Type" in text:
            m = re.search(r'Processor Type\.?\s*[-:]\s*(.*?)\s*(?=RAM\s*[-:])', text, re.IGNORECASE)
            if m:
                return m.group(1).strip()
        else:
            # For Startech or generic, look for "Processor:" pattern.
            m = re.search(r'Processor\s*[-:]\s*([^\n,]+)', text, re.IGNORECASE)
            if m:
                return m.group(1).strip()
        return None

    def extract_ram(self, text: str):
        text = str(text)
        # Look for pattern like "RAM - 16GB" (allowing optional spaces)
        m = re.search(r'RAM\s*[-:]\s*([\d]+)\s*GB', text, re.IGNORECASE)
        if m:
            return m.group(1).strip() + "GB"
        return None

    def extract_storage(self, text: str):
        text = str(text)
        # Look for "Storage" followed by a dash/colon and capture up to a delimiter.
        m = re.search(r'Storage\s*[-:]\s*([^\n,;]+)', text, re.IGNORECASE)
        if m:
            storage_text = m.group(1).strip()
            # Remove extra parts by splitting on common keywords:
            # For example, if storage_text is "512GB Gen 4 SSD Graphics: NVIDIA RTX 4070 8GB GDDR6",
            # we want just "512GB Gen 4 SSD"
            storage_clean = re.split(r'\s+(?:Graphics|Display|Licensed Application|Features|Camera)\b', storage_text, flags=re.IGNORECASE)[0]
            return storage_clean.strip()
        return None

    def extract_display(self, text: str):
        text = str(text)
        # First try for Ryans format: "Display Size (Inch) - <value>"
        if "Display Size" in text:
            m = re.search(r'Display Size\s*\(Inch\)\s*[-:]\s*([\d\.]+)', text, re.IGNORECASE)
            if m:
                # Optionally, you could capture more (e.g., additional words) if needed.
                display_val = m.group(1).strip()
                return display_val + " inch"
        else:
            # For Startech or generic format, look for "Display:" pattern.
            m = re.search(r'Display\s*[-:]\s*([^\n]+)', text, re.IGNORECASE)
            if m:
                display_text = m.group(1).strip()
                # Remove extra details after keywords such as "Licensed Application", "Graphics", "Features", etc.
                display_clean = re.split(r'\s+(?:Licensed Application|Graphics|Features|Touch[-\s]?Screen|with)\b', display_text, flags=re.IGNORECASE)[0]
                return display_clean.strip()
        return None

    def extract_features(self):
        processors = []
        rams = []
        storages = []
        displays = []
        
        for tech_details in tqdm(self.df['Cleaned_Tech_Details'], desc="Extracting features"):
            proc = self.extract_processor(tech_details)
            ram = self.extract_ram(tech_details)
            stor = self.extract_storage(tech_details)
            disp = self.extract_display(tech_details)
            
            processors.append(proc)
            rams.append(ram)
            storages.append(stor)
            displays.append(disp)
        
        self.df['Processor'] = processors
        self.df['RAM'] = rams
        self.df['Storage'] = storages
        self.df['Display'] = displays
        
        print("[FeatureExtractor] Feature extraction complete.")
        return self.df
