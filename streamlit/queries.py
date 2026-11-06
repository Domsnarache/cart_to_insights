import pandas as pd
import streamlit as st
from sqlalchemy.engine.base import Engine


@st.cache_data
def load_overview_kpis(_engine: Engine) -> pd.DataFrame:
    query: str = """
    SELECT 
        COUNT(DISTINCT o.order_id) AS total_orders,
        ROUND(SUM(p.payment_value), 2) AS total_revenue,
        COUNT(DISTINCT c.customer_unique_id) AS total_customers,
        ROUND(SUM(p.payment_value) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
    FROM orders o
    JOIN order_payments p ON o.order_id = p.order_id
    JOIN customers c ON o.customer_id = c.customer_id;
    """
    df_kpi: pd.DataFrame = pd.read_sql(query, con=_engine)
    return df_kpi


@st.cache_data
def load_monthly_sales(_engine: Engine) -> pd.DataFrame:
    query: str = """
    SELECT 
        SUBSTRING(o.order_purchase_timestamp, 1, 7) AS order_month,
        ROUND(SUM(p.payment_value), 2) AS revenue,
        COUNT(DISTINCT o.order_id) AS orders
    FROM orders o
    JOIN order_payments p ON o.order_id = p.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY order_month
    ORDER BY order_month;
    """
    df_sales: pd.DataFrame = pd.read_sql(query, con=_engine)
    return df_sales


@st.cache_data
def load_top_categories(_engine: Engine) -> pd.DataFrame:
    query: str = """
    SELECT 
        p.product_category_name_english AS category,
        ROUND(SUM(oi.price), 2) AS revenue,
        COUNT(DISTINCT oi.order_id) AS order_count
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    WHERE p.product_category_name_english IS NOT NULL
    GROUP BY category
    ORDER BY revenue DESC
    LIMIT 10;
    """
    df_categories: pd.DataFrame = pd.read_sql(query, con=_engine)
    return df_categories


@st.cache_data
def load_customers_by_state(_engine: Engine) -> pd.DataFrame:
    query: str = """
    SELECT 
        customer_state AS state,
        COUNT(customer_unique_id) AS customer_count
    FROM customers
    GROUP BY customer_state
    ORDER BY customer_count DESC
    LIMIT 10;
    """
    df_states: pd.DataFrame = pd.read_sql(query, con=_engine)
    return df_states


@st.cache_data
def load_top_sellers(_engine: Engine) -> pd.DataFrame:
    query: str = """
    SELECT 
        s.seller_id AS seller,
        s.seller_state AS state,
        ROUND(SUM(oi.price), 2) AS total_sales,
        COUNT(DISTINCT oi.order_id) AS order_count
    FROM order_items oi
    JOIN sellers s ON oi.seller_id = s.seller_id
    GROUP BY s.seller_id, s.seller_state
    ORDER BY total_sales DESC
    LIMIT 10;
    """
    df_sellers: pd.DataFrame = pd.read_sql(query, con=_engine)
    return df_sellers


@st.cache_data
def load_delivery_performance(_engine: Engine) -> pd.DataFrame:
    query: str = """
    SELECT 
        CASE 
            WHEN order_delivered_customer_date > order_estimated_delivery_date THEN 'Delayed'
            ELSE 'On-Time'
        END AS delivery_status,
        COUNT(DISTINCT o.order_id) AS order_count,
        ROUND(AVG(r.review_score), 2) AS avg_rating
    FROM orders o
    JOIN order_reviews r ON o.order_id = r.order_id
    WHERE o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL
    GROUP BY delivery_status;
    """
    df_delivery: pd.DataFrame = pd.read_sql(query, con=_engine)
    return df_delivery


@st.cache_data
def load_review_distribution(_engine: Engine) -> pd.DataFrame:
    query: str = """
    SELECT 
        review_score,
        COUNT(*) AS review_count
    FROM order_reviews
    GROUP BY review_score
    ORDER BY review_score;
    """
    df_reviews: pd.DataFrame = pd.read_sql(query, con=_engine)
    return df_reviews
