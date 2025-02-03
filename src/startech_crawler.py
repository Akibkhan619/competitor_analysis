import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm  # For progress bar

# Setup Selenium Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no browser window)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
service.start()
time.sleep(5)  # Give extra time to start the service
driver = webdriver.Chrome(service=service, options=chrome_options)

# Base URL for StarTech laptops
BASE_URL = "https://www.startech.com.bd/laptop-notebook?page="

# Ensure data/raw/ directory exists
os.makedirs("../data/raw", exist_ok=True)

# File paths
RAW_DATA_FILE = "../data/raw/startech_laptops_raw.csv"
URLS_FILE = "../data/raw/startech_product_links.txt"

# Function to fetch all product links
def get_product_links():
    product_links = []

    for page in range(1, 32):  # Pages 1 to 31
        print(f"\n🔍 Crawling page {page}...")
        driver.get(BASE_URL + str(page))
        time.sleep(2)  # Allow page to load

        # Wait for product container to appear
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "p-item-name"))
        )

        # Extract product links
        product_divs = driver.find_elements(By.CSS_SELECTOR, ".p-item-name a")
        page_links = [div.get_attribute("href") for div in product_divs if div.get_attribute("href")]

        # Avoid duplicates
        for link in page_links:
            if link not in product_links:
                product_links.append(link)

        print(f"✅ Page {page} - Found {len(page_links)} new product links (Total so far: {len(product_links)})")

    # Save URLs to a text file
    with open(URLS_FILE, "w") as f:
        for url in product_links:
            f.write(url + "\n")

    print(f"\n📄 Product URLs saved to {URLS_FILE}")
    
    return product_links

# Function to extract product details
def get_product_details(product_url, product_index, total_products):
    driver.get(product_url)
    time.sleep(2)

    try:
        product_name = driver.find_element(By.XPATH, "//h1[@itemprop='name']").text.strip()
    except:
        product_name = "N/A"

    try:
        price_element = driver.find_element(By.CLASS_NAME, "product-price")
        price = price_element.text.strip() if price_element else "N/A"
    except:
        price = "N/A"

    try:
        technical_details_element = driver.find_element(By.CLASS_NAME, "short-description")
        technical_details = technical_details_element.text.strip() if technical_details_element else "N/A"
    except:
        technical_details = "N/A"

    try:
        description_element = driver.find_element(By.ID, "description")
        description = description_element.text.strip() if description_element else "N/A"
    except:
        description = "N/A"

    print(f"🛒 Fetching product {product_index}/{total_products}: {product_name}")

    return {
        "URL": product_url,
        "Product Name": product_name,
        "Price": price,
        "Technical Details": technical_details,
        "Description": description
    }

# Start Scraping
print("\n🚀 Fetching product links...")
product_links = get_product_links()

print("\n📊 Fetching product details...\n")
products_data = []
for i, link in tqdm(enumerate(product_links, start=1), total=len(product_links), desc="🔄 Crawling Products"):
    product_details = get_product_details(link, i, len(product_links))
    if product_details:
        products_data.append(product_details)
    time.sleep(1)  # Prevent overloading the website

# Close WebDriver
driver.quit()

# Save data to CSV
df = pd.DataFrame(products_data)
df.to_csv(RAW_DATA_FILE, index=False)

print(f"\n✅ Scraping completed! Data saved in '{RAW_DATA_FILE}'.")
