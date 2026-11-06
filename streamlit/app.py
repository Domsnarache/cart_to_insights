import plotly.express as px
import streamlit as st

from database import get_database_engine
import queries as q
import utils as u

st.set_page_config(page_title="Cart2Insights Dashboard", layout="wide")

st.title("Cart2Insights: E-Commerce Performance Intelligence")
st.markdown("Executive Data Analytics Dashboard analyzing 100,000+ Brazilian E-Commerce transactions from MySQL.")

engine = get_database_engine()

# Macro KPI Metrics
kpi_df = q.load_overview_kpis(engine)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", u.format_currency(kpi_df["total_revenue"].iloc[0]))
col2.metric("Total Orders", u.format_number(int(kpi_df["total_orders"].iloc[0])))
col3.metric("Total Customers", u.format_number(int(kpi_df["total_customers"].iloc[0])))
col4.metric("Average Order Value (AOV)", u.format_currency(kpi_df["avg_order_value"].iloc[0]))

st.divider()

# Analytical Dimensions
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview", 
    "Sales Analysis", 
    "Customer Analysis", 
    "Seller & Product", 
    "Delivery Logistics", 
    "Customer Experience"
])

# Tab 1: Executive Overview
with tab1:
    st.subheader("Platform Health Overview")
    st.info("The Cart2Insights platform has processed over R$ 16.0M BRL across ~100,000 orders. The marketplace operates with a 3.12% repeat purchase retention rate, indicating strong new customer acquisition with substantial opportunity for lifecycle retention programs.")
    
    sales_df = q.load_monthly_sales(engine)
    fig_overview = px.line(
        sales_df, 
        x="order_month", 
        y="revenue", 
        title="Revenue Trajectory (2016 - 2018)", 
        markers=True
    )
    st.plotly_chart(fig_overview, width="stretch")

# Tab 2: Sales & Revenue Analysis
with tab2:
    st.subheader("Monthly Revenue Trends and Top Product Categories")
    
    sales_df = q.load_monthly_sales(engine)
    fig_trend = px.line(
        sales_df, 
        x="order_month", 
        y="revenue", 
        title="Monthly Revenue Trend (BRL)", 
        markers=True
    )
    st.plotly_chart(fig_trend, width="stretch")
    
    cat_df = q.load_top_categories(engine)
    fig_cat = px.bar(
        cat_df, 
        x="revenue", 
        y="category", 
        orientation="h", 
        title="Top 10 Product Categories by Revenue (BRL)",
        color="revenue",
        color_continuous_scale="Viridis"
    )
    fig_cat.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_cat, width="stretch")

# Tab 3: Customer Geographic & Retention Analysis
with tab3:
    st.subheader("Customer Geographic Distribution & Retention Patterns")
    
    state_df = q.load_customers_by_state(engine)
    fig_state = px.bar(
        state_df, 
        x="state", 
        y="customer_count", 
        title="Top 10 Customer States by Unique Buyer Count", 
        color="customer_count", 
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_state, width="stretch")
    
    st.warning("Retention Insight: 96.88% of buyers are One-Time Customers, while only 3.12% return for repeat purchases. The Southeast region (SP, RJ, MG) accounts for over 66% of all orders.")

# Tab 4: Seller & Product Catalog Dynamics
with tab4:
    st.subheader("Merchant Revenue Performance & Concentration")
    
    seller_df = q.load_top_sellers(engine)
    
    short_labels: list[str] = []
    for seller_id in seller_df["seller"]:
        clean_label: str = u.shorten_id(seller_id, length=8)
        short_labels.append(clean_label)
    
    seller_df["seller_label"] = short_labels
    
    fig_sellers = px.bar(
        seller_df, 
        x="seller_label", 
        y="total_sales", 
        color="state", 
        title="Top 10 Merchants by Gross Sales (BRL)",
        hover_data={"seller": True, "seller_label": False, "total_sales": ":.2f", "state": True},
        labels={"seller_label": "Seller (Short ID)", "total_sales": "Gross Sales (BRL)", "seller": "Full Seller ID"}
    )
    st.plotly_chart(fig_sellers, width="stretch")

# Tab 5: Delivery Logistics & Transit Latency
with tab5:
    st.subheader("Fulfillment Timeliness and Carrier Delivery Performance")
    
    deliv_df = q.load_delivery_performance(engine)
    fig_deliv = px.bar(
        deliv_df, 
        x="delivery_status", 
        y="order_count", 
        color="delivery_status", 
        title="Order Fulfillment Volume: On-Time vs Delayed Deliveries",
        color_discrete_map={"On-Time": "#2ecc71", "Delayed": "#e74c3c"}
    )
    st.plotly_chart(fig_deliv, width="stretch")

# Tab 6: Customer Experience & Satisfaction Analysis
with tab6:
    st.subheader("Customer Satisfaction, Review Ratings & Delay Impact")
    
    review_df = q.load_review_distribution(engine)
    fig_reviews = px.bar(
        review_df, 
        x="review_score", 
        y="review_count", 
        title="Customer Review Rating Distribution (1 to 5 Stars)",
        color="review_score",
        color_continuous_scale="Teal"
    )
    st.plotly_chart(fig_reviews, width="stretch")
    
    fig_rating = px.bar(
        deliv_df, 
        x="delivery_status", 
        y="avg_rating", 
        color="delivery_status", 
        title="Customer Satisfaction Impact: On-Time (4.29 Stars) vs Delayed (2.57 Stars)",
        color_discrete_map={"On-Time": "#2ecc71", "Delayed": "#e74c3c"}
    )
    st.plotly_chart(fig_rating, width="stretch")
