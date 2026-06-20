# 🍲 Local Food Wastage Management System

A data-driven platform that connects surplus food providers with receivers (NGOs and individuals) to reduce food wastage.

## 🔗 Live App
[Click here to open the app](https://food-wastage-management-esaljuwbnnc9pm7urzfqts.streamlit.app/)

## 📌 Problem Statement
Many restaurants and households discard surplus food while people struggle with food insecurity. This system bridges that gap by listing surplus food and allowing receivers to claim it.

## 🛠️ Tech Stack
- **SQL (SQLite)** — core database, all queries and analysis
- **Python** — data loading and Streamlit app
- **Streamlit** — interactive web interface
- **Pandas** — connecting SQL results to the app
- **Matplotlib** — charts in the analysis notebook

## 📂 Project Structure
food-wastage-management/

├── data/                          # CSV datasets

│   ├── providers_data.csv

│   ├── receivers_data.csv

│   ├── food_listings_data.csv

│   └── claims_data.csv

├── schema.sql                     # Database table definitions

├── queries.sql                    # All 15 SQL queries

├── master.sql                     # Complete SQL file (schema + CRUD + queries)

├── food_wastage_analysis.ipynb    # SQL analysis notebook with outputs and charts

├── load_data.py                   # Loads CSV data into SQLite

├── queries.py                     # SQL queries used by Streamlit app

├── app.py                         # Main Streamlit application

├── requirements.txt               # Python dependencies

└── food.db                        # SQLite database
## 🗄️ Database Schema
- **providers** — food providers (restaurants, grocery stores, supermarkets)
- **receivers** — NGOs and individuals receiving food
- **food_listings** — available food items with expiry date and quantity
- **claims** — food claims made by receivers with status tracking

## 📊 Streamlit App Features
- **Overview page** — key metrics and claim status pie chart
- **Browse & Filter** — filter food by city, provider, food type, meal type
- **CRUD operations** — add, update, delete food listings
- **SQL Insights** — all 15 SQL queries with results and bar charts
- **Contact Directory** — provider and receiver contact details

## 🔍 15 SQL Queries Covered
1. Providers and receivers count per city
2. Which provider type contributes the most food
3. Receivers who have claimed the most food
4. Total quantity of food available
5. City with the highest number of food listings
6. Most commonly available food types
7. Number of claims made per food item
8. Provider with the most successful claims
9. Percentage of claims by status
10. Average quantity of food claimed per receiver
11. Which meal type is claimed the most
12. Total quantity of food donated by each provider
13. Food items expiring within the next 7 days
14. Top providers by number of listings
15. Receivers and their city distribution

## 📓 SQL Analysis Notebook
The `food_wastage_analysis.ipynb` notebook contains:
- All 15 SQL queries with their actual output tables
- 3 visualizations — provider type chart, claim status pie chart, meal type chart
- Run locally to see all query outputs from the real database

## ▶️ How to Run Locally
```bash
# 1. Clone the repository
git clone https://github.com/Soham006/food-wastage-management.git
cd food-wastage-management

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Load data into database
python load_data.py

# 5. Run the app
streamlit run app.py
```

## 📁 Dataset
| Dataset | Description | Records |
|---------|-------------|---------|
| providers_data.csv | Food providers details | 1000 |
| receivers_data.csv | Receivers details | 1000 |
| food_listings_data.csv | Available food listings | 1000 |
| claims_data.csv | Food claims records | 1000 |