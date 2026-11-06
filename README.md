# Cart to Insights - E-Commerce Data Analysis

This is a data analysis project based on the Brazilian Olist e-commerce dataset (around 100,000 orders from 2016 to 2018).

I built this project to practice working with real-world data: cleaning messy CSV files, storing them in a relational database, running SQL queries to answer business questions, and building a simple dashboard to visualize the results.

## What I Did

1. Cleaned the raw data: fixed missing values, converted date columns, and removed duplicates across 9 tables.
2. Stored the cleaned tables in MySQL with primary and foreign keys.
3. Wrote SQL queries using joins, CTEs, and window functions to analyze sales, orders, and delivery times.
4. Created calculated columns like delivery delay and customer retention.
5. Ran exploratory data analysis (EDA) and basic hypothesis testing (T-Test, ANOVA, Chi-Square).
6. Built an interactive dashboard using Streamlit to display charts and key metrics.

## Tools Used

- Python (pandas, matplotlib, seaborn, plotly, scipy)
- MySQL (with SQLAlchemy and PyMySQL)
- Streamlit
- Git and GitHub

## Project Structure

```
cart_to_insights/
├── data/
│   ├── raw/                  # Original CSV files from Kaggle
│   └── cleaned/              # Cleaned CSV files ready for MySQL
├── docs/
│   └── ERD_diagram.md        # Database schema and table relationships
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_quality_analysis.ipynb
│   ├── 03_data_cleaning.ipynb
│   ├── 04_sql_analysis.ipynb
│   ├── 05_feature_engineering.ipynb
│   ├── 06_eda.ipynb
│   └── 07_statistical_analysis.ipynb
├── streamlit/
│   ├── app.py                # Main Streamlit dashboard
│   ├── database.py           # MySQL database connection helper
│   ├── queries.py            # SQL queries used in the dashboard
│   └── utils.py              # Helper functions for formatting numbers
├── requirements.txt
└── README.md
```

## Dataset

The data comes from the [Brazilian E-Commerce Public Dataset by Olist on Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). It contains 9 tables:
- Customers
- Orders
- Order items
- Payments
- Reviews
- Products
- Sellers
- Geolocation
- Category name translations

To check how the tables connect with each other, see [docs/ERD_diagram.md](docs/ERD_diagram.md). Download the raw CSVs from Kaggle and place them in `data/raw/` before running the notebooks.

## Key Insights from the Data

- Delivery delays have a big impact on reviews: On-time orders averaged 4.25 stars, but delayed orders dropped down to 2.28 stars.
- Most buyers do not return: About 96.9% of customers only bought once, while only ~3.1% made repeat purchases.
- Bank slip payments have higher cancellation rates: Boleto (bank slip) orders get cancelled more often than credit card orders, likely because people forget to pay before the slip expires.

## How to Run This Project

### 1. Clone the repository and set up Python
```
# Clone the repo and navigate into the project directory
cd cart_to_insights

# Create and activate virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure MySQL
The database connection string in `streamlit/database.py` and the notebooks defaults to:
`mysql+pymysql://root:1234@localhost:3306/ecommerce_db`

Update the username, password, or port if your local MySQL setup is different.

### 3. Run the notebooks
Run the notebooks in `notebooks/` in order from `01_` to `07_` to clean the data and load it into MySQL.

### 4. Run the Streamlit dashboard
```
streamlit run streamlit/app.py
```
Open `http://localhost:8501` in your browser to view the dashboard.
