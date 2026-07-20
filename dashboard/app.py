import os

import pandas as pd
import psycopg2
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="GemRadar AI",
    page_icon="💎",
    layout="wide"
)


@st.cache_resource
def connect_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


conn = connect_db()

query = """
SELECT
    name,
    symbol,
    ai_score,
    risk_level,
    gem_score,
    gem_status,
    liquidity,
    volume_24h,
    fdv
FROM tokens
ORDER BY gem_score DESC NULLS LAST, ai_score DESC
LIMIT 10;
"""

df = pd.read_sql(query, conn)

st.title("💎 GemRadar AI")
st.subheader("Top 10 Meme Coins")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Tokens", len(df))

with col2:
    watchlist = len(df[df["gem_status"].fillna("").str.contains("WATCHLIST")])
    st.metric("Watchlist", watchlist)

with col3:
    hot = len(df[df["gem_score"].fillna(0) >= 80])
    st.metric("Hot Gems", hot)

st.divider()

st.dataframe(df, use_container_width=True)