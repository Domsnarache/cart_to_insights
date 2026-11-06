import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine


@st.cache_resource
def get_database_engine() -> Engine:
    connection_url: str = "mysql+pymysql://root:1234@localhost:3306/ecommerce_db"
    engine: Engine = create_engine(connection_url)
    return engine
