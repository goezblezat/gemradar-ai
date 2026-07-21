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
st.caption("AI Meme Coin Scanner")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📦 Total Tokens", len(df))

with col2:
    watchlist = len(
        df[df["gem_status"].fillna("").str.contains("WATCHLIST")]
    )
    st.metric("👀 Watchlist", watchlist)

with col3:
    hot = len(df[df["gem_score"].fillna(0) >= 80])
    st.metric("🔥 Hot Gems", hot)

with col4:
    avg_ai = round(df["ai_score"].fillna(0).mean(), 1)
    st.metric("🤖 Avg AI", avg_ai)

st.divider()
search = st.text_input(
    "🔍 Search Token",
    placeholder="Contoh: SOL atau Tomato"
)

if search:
    df = df[
        df["name"].str.contains(search, case=False, na=False)
        |
        df["symbol"].str.contains(search, case=False, na=False)
    ]
st.subheader("📋 Top Meme Coins")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)