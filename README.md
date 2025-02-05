# **Laptop Data Analysis and Recommender System**

## **📌 Overview**
This project involves **crawling, cleaning, feature extraction, SWOT analysis, and recommendation** for laptops sold by **two of Bangladesh's top computer retailers**:
- **Ryans Computers** (`ryans.com`)
- **Startech Computers** (`startech.com.bd`)

The system scrapes **laptop product details**, cleans the data, extracts key specifications, generates **SWOT analyses using Google Gemini API**, and provides a **personalized recommendation system using LLM embeddings and cosine similarity**.

---

## **🚀 Features**
### **1️⃣ Crawling Laptop Data**
- Scrapes laptop details from **Ryans Computers** and **Startech Computers**.
- Extracts **product name, price, technical details, and descriptions**.
- **Saves raw data** in `data/raw/`.

📂 **Code:**
- [`src/ryans_crawler.py`](src/ryan_crawler.py)  
- [`src/startech_crawler.py`](src/startech_crawler.py) (if added)

---

### **2️⃣ Data Cleaning**
- Converts **Bangla numerals** to **English**.
- Cleans **price** format.
- Removes **unwanted promotional text** from product descriptions.
- Saves **cleaned data** in `data/processed/combined_data_cleaned.xlsx`.

📂 **Code:**
- [`modules/data_clean.py`](modules/data_cleaner.py)

---

### **3️⃣ Feature Extraction**
- Extracts key **laptop features** from `Cleaned_Tech_Details`, including:
  - **Processor** (e.g., "Intel Core i5 12th Gen")
  - **RAM** (e.g., "8GB DDR4")
  - **Storage** (e.g., "512GB SSD")
  - **Display** (e.g., "15.6-inch FHD")

📂 **Code:**
- [`modules/feature_extractor.py`](modules/feature_extractor.py)

---

### **4️⃣ SWOT Analysis (Google Gemini API)**
- Uses **Google Gemini API** to generate **Strengths, Weaknesses, Opportunities, and Threats** (SWOT) for each laptop.
- Saves the **SWOT analysis** as a new column.

📂 **Code:**
- [`generate_swot.py`](swot_generator.py)

---

### **5️⃣ Laptop Recommendation System**
- Uses **Sentence Transformers (Embeddings) and Cosine Similarity** to recommend the **top 3 most relevant laptops** for a given query.
- Stores laptop **embeddings** in a Pickle file (`.pkl`) for efficient lookup.
- Reads **query from a JSON config file** and returns **best-matching laptops**.

📂 **Code:**
- [`modules/laptop_recommender.py`](modules/laptop_recommender.py)
- [`save_embeddings.py`](save_embeddings.py)
- [`recommend_laptops.py`](recommend_laptops.py)

---

## **🛠️ Setup & Usage**
### **1️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2️⃣ Crawl Data**
```bash
python src/ryans_crawler.py
python src/startech_crawler.py
```

### **3️⃣ Clean Data and Extract Features**
```bash
python data_prepare.py
```

### **4️⃣ Generate SWOT Analysis**
```bash
python generate_swot.py
```
📄 Output stored in: outputs/laptops_swot_output.xlsx


### **5️⃣ Generate Embeddings (One-time)**
```bash
python save_embeddings.py
```

### **6️⃣ Run Laptop Recommendation**
Edit config/recommender_config.json to add a query:
```bash
{
    "embedding_file": "data/processed/laptop_embeddings.pkl",
    "query": "I need a 15-inch white laptop with 8GB RAM and SSD"
}
```

then run 
```bash
python recommend_laptops.py
```
📄 Output stored in: `outputs/recommendation_report.txt`

📄 Sample Recommendation Output `outputs/recommendation_report.txt`

```bash
📌 Laptop Recommendation Report
==================================================
🔍 **Query:** I want a buy 15-inch white laptop with 8GB RAM and 512 SSD

🎯 **Top Recommended Laptops:**

1. **HP 15-fd0292TU Intel Core i5 1334U 8GB RAM 512GB SSD 15.6 Inch FHD Display Moonlight Blue Laptop**
   - **Price:** 71000.0 BDT
   - **Tech Details:**  Processor Type. - Core i5 Generation - 13th (Intel) RAM - 8GB Storage - 512GB SSD Graphics Memory - Shared Display Size (Inch) - 15.6 
   - **Description:** The HP 15-fd0292TU Intel Core i5 Moonlight Blue Laptop is a reliable option for everyday tasks. Its 15.6-inch FHD display offers clear visuals while the 8GB RAM ensures smooth multitasking. With a 512GB SSD you get fast storage and quick boot times. It’s a laptop that fits well into daily life providing both performance and style. Benefits & Features Powerful Processor: The Intel Core i5 13th Gen processor delivers efficient performance for work and play. High-Quality Display: The 15.6-inch FHD LED screen with 1920x1080 resolution offers sharp, vibrant visuals. Ample Memory: 8GB DDR4 RAM supports seamless multitasking, even with demanding applications. Fast Storage: A 512GB SSD ensures quick startup times and rapid file access. Sleek Design: The Moonlight Blue finish gives it a stylish, modern look. Enhanced Graphics: Intel Iris Xe Graphics handles everyday graphic tasks and light gaming well. Portable: Lightweight and easy to carry making it ideal for students and professionals on the go. What You Need to Know Before Hitting 'Add to Cart' Compatibility: Make sure your software and accessories are compatible with Windows. Upgrade Options: Consider future upgrades, like increasing RAM if needed. Battery Life: Check the battery life to see if it meets your needs. Warranty: Review the warranty terms for coverage details. Software: It comes with Windows, but you may need to install additional software. Sum it up This laptop offers solid performance with a sleek design. It’s reliable for daily use. The HP 15-fd0292TU Intel Core i5 Moonlight Blue Laptop is a great choice for work and study. Its features make it stand out. What is the price of HP 15-fd0292TU Laptop In Bangladesh? The price of HP 15-fd0292TU Laptop starts from 71,000 . The price may vary due to your customization and product availability. 
   - **Product Link:** https://www.ryans.com/hp-15-fd0292tu-intel-core-i5-1334u-15.6-inch-moonlight-blue-laptop
==================================================
2. **Asus VivoBook Go 15 E1504FA AMD Ryzen 5 7520U 8GB RAM 512GB SSD 15.6 Inch FHD LED Display Mixed Black Laptop**
   - **Price:** 66500.0 BDT
   - **Tech Details:**  Processor Type. - Ryzen 5 Generation - Ryzen RAM - 8GB Storage - 512GB SSD Graphics Memory - Shared Display Size (Inch) - 15.6 
   - **Description:** Looking for a budget-friendly laptop that offers powerful performance and sleek design? The Asus VivoBook Go 15 E1504FA AMD Ryzen 5 7520U 8GB RAM 512GB SSD 15.6 Inch FHD LED Display Mixed Black Laptop is the perfect fit for your needs. This laptop features the AMD Ryzen 5 7520U processor, 8GB RAM, and 512GB SSD. It is great for smooth multitasking and fast performance for work, study, and entertainment. The 15.6-inch Full HD LED display provides stunning visuals, while the stylish Mixed Black color gives it a modern and professional look. Key Features That Make the Asus VivoBook Go 15 E1504FA Stand Out The Asus VivoBook Go 15 E1504FA is built to provide excellent smooth performance for everyday tasks. This laptop handles multitasking and productivity seamlessly. Whether you're working on office documents, streaming movies, or browsing the web, the AMD Ryzen 5 keeps everything running smoothly. With 8GB RAM, the laptop lets you effortlessly switch between apps and handle several tasks at once without slowdowns. The 512GB SSD ensures ultra-fast storage performance, allowing for quicker boot-ups, file transfers, and improved overall system responsiveness compared to traditional hard drives. The 15.6-inch Full HD LED display gives you vibrant, clear visuals, ideal for work, video calls, and entertainment. The AMD Radeon Graphics enhances the laptop’s performance, making it suitable for light gaming, basic photo editing, and watching HD content. How to Buy the Asus VivoBook Go 15 E1504FA Get your hands on the Asus VivoBook Go 15 E1504FA AMD Ryzen 5 laptop at Ryans Computers in Bangladesh today! With its exceptional performance, fast SSD storage, and stunning Full HD display, this laptop is the perfect companion for all your tasks. Visit us now to enjoy a great deal on the best performance in the budget laptop category. Make the Smart Choice with the Asus VivoBook Go 15 The Asus VivoBook Go 15 E1504FA AMD Ryzen 5 7520U 8GB RAM 512GB SSD 15.6 Inch FHD LED Display Mixed Black Laptop is your go-to budget-friendly laptop for both work and entertainment. With its 8GB RAM, 512GB SSD, and Full HD display, you can count on smooth performance and reliability. Whether you need it for professional tasks or casual use, this laptop provides great value without compromising on quality. Visit Ryans Computers in Bangladesh today and grab your Asus VivoBook Go 15 for unbeatable value! What is the price of Asus VivoBook Go 15 E1504FA Laptop In Bangladesh? The price of Asus VivoBook Go 15 E1504FA Laptop starts from 66,500 . The price may vary due to your customization and product availability. 
   - **Product Link:** https://www.ryans.com/asus-vivobook-go-15-e1504fa-amd-ryzen-5-7520u-15.6-inch-mixed-black-laptop
==================================================
3. **Lenovo IdeaPad Slim 3i 15IRH8 13th Gen Intel Core i5 13420H 16GB, 512GB SSD15.6 Inch FHD Display Arctic Grey Laptop**
   - **Price:** 79500.0 BDT
   - **Tech Details:**  Processor Type. - Core i5 Generation - 13th (Intel) RAM - 16GB Storage - 512GB SSD Graphics Memory - Shared Display Size (Inch) - 15.6 
   - **Description:** The Lenovo IdeaPad Slim 3i 15IRH8 is a budget-friendly laptop that offers good value for money. It has a sleek and stylish design, and it is powered by a 13th Gen Intel Core i5 processor. The laptop also has 16GB of RAM and a 512GB SSD, which should be enough for most users. What Makes Lenovo IdeaPad Slim 3i 15IRH8 Laptop Stand Out? The Lenovo IdeaPad Slim 3i 15IRH8 is a good choice for users who are looking for a budget-friendly laptop with a decent amount of performance. The laptop is powered by a 13th Gen Intel Core i5 processor, which is a good choice for everyday tasks such as browsing the web, checking email, and editing documents. The laptop also has 16GB of RAM and a 512GB SSD, which should be enough for most users. Who Should Buy an Lenovo IdeaPad Slim 3i 15IRH8 Laptop? The Lenovo IdeaPad Slim 3i 15IRH8 is a good choice for users who are looking for a budget-friendly laptop with a decent amount of performance. The laptop is not suitable for gaming or other demanding tasks, but it is a good choice for everyday tasks such as browsing the web, checking email, and editing documents. Here are some additional things to consider when deciding whether or not to buy the Lenovo IdeaPad Slim 3i 15IRH8: The laptop's battery life is up to 10 hours. This is a good battery life for a laptop in this price range. The laptop has a 15.6 inch FHD display. This is a good display for everyday tasks such as watching movies and browsing the web. The laptop is available in Arctic Grey. This is a sleek and stylish color. The Lenovo IdeaPad Slim 3i 15IRH8 is a good choice for users who are looking for a budget-friendly laptop with a decent amount of performance. What is the price of Lenovo IdeaPad Slim 3i 15IRH8 Laptop In Bangladesh? The price of Lenovo IdeaPad Slim 3i 15IRH8 Laptop starts from 79,500 . The price may vary due to your customization and product availability. 
   - **Product Link:** https://www.ryans.com/lenovo-ideapad-slim-3i-15irh8-13th-gen-intel-core-i5-13420h-arctic-grey-laptop
==================================================

```

## **🎯 Next Steps**
- **Optimize Crawling**: Add **proxy rotation** & **dynamic delays** to avoid crawling bans.
- **Batch API Calls**: Reduce **Google Gemini API** calls using batch requests.
- **Improve Recommendations**: Use **RAG-based retrieval** as I have the infomation of laptops. Sending this information with prompt will increase the models'output.**.
- **Deploy Web UI**: Build a **Streamlit or Flask interface** for easy interaction.
