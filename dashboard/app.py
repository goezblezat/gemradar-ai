import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import pandas as pd
import psycopg2
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from dotenv import load_dotenv

from ai.recommendation import get_recommendation

load_dotenv()

st.set_page_config(
    page_title="GemRadar AI",
    page_icon="💎",
    layout="wide"
)
# Refresh otomatis setiap 30 detik
st_autorefresh(interval=30000, key="dashboard_refresh")
def score_color(score):
    if score >= 80:
        return "🟢"
    elif score >= 60:
        return "🟡"
    return "🔴"

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
# Format angka agar mudah dibaca
df["liquidity"] = df["liquidity"].fillna(0).map(lambda x: f"${x:,.0f}")
df["volume_24h"] = df["volume_24h"].fillna(0).map(lambda x: f"${x:,.0f}")
df["fdv"] = df["fdv"].fillna(0).map(lambda x: f"${x:,.0f}")

df["ai_score"] = df["ai_score"].fillna(0).astype(int)
df["gem_score"] = df["gem_score"].fillna(0).astype(int)

st.title("💎 GemRadar AI")
st.caption("AI Meme Coin Scanner")
if st.button("🔄 Refresh Data"):
    st.rerun()

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
st.divider()

st.subheader("🏆 Top Gems Today")


top3 = (
    df.sort_values(
        by=["gem_score", "ai_score"],
        ascending=False
    )
    .head(3)
)
best = top3.iloc[0]
recommendation = get_recommendation(
    best["gem_score"],
    best["ai_score"],
    best["risk_level"].replace("🟢 LOW","LOW")
                     .replace("🟡 MEDIUM","MEDIUM")
                     .replace("🔴 HIGH","HIGH")
                     .replace("⚪ UNKNOWN","UNKNOWN"),
    70000,
    12000,
    250000
)

st.success(
    f"💎 Best Gem Right Now : {best['name']} "
    f"| Gem Score {best['gem_score']} "
    f"| AI Score {best['ai_score']}"
)
st.info(f"⭐ {recommendation['signal']}")

for reason in recommendation["reasons"]:
    st.write(reason)

col1, col2, col3 = st.columns(3)
col1, col2, col3 = st.columns(3)

medals = ["🥇", "🥈", "🥉"]
cols = [col1, col2, col3]

for i, (_, row) in enumerate(top3.iterrows()):

    with cols[i]:

        st.markdown(f"### {medals[i]} {row['name']}")

        st.metric(
            f"{score_color(row['gem_score'])} Gem Score",
            row["gem_score"]
        )

        st.metric(
            f"{score_color(row['ai_score'])} AI Score",
            row["ai_score"]
        )

        st.caption(row["risk_level"])
st.subheader("📋 Top Meme Coins")
# Risk Badge
df["risk_level"] = (
    df["risk_level"]
    .fillna("UNKNOWN")
    .replace({
        "LOW": "🟢 LOW",
        "MEDIUM": "🟡 MEDIUM",
        "HIGH": "🔴 HIGH",
        "UNKNOWN": "⚪ UNKNOWN"
    })
)

# Gem Status Badge
df["gem_status"] = (
    df["gem_status"]
    .fillna("-")
    .replace({
        "WATCHLIST": "👀 WATCHLIST",
        "👀 WATCHLIST": "👀 WATCHLIST",
        "HOT": "🔥 HOT",
        "HOT GEM": "🔥 HOT GEM",
        "GEM": "💎 GEM",
        "IGNORE": "❌ IGNORE",
        "-": "-"
    })
)
display_df = df.rename(
    columns={
        "name": "🪙 Token",
        "symbol": "💰 Symbol",
        "ai_score": "🤖 AI",
        "gem_score": "💎 Gem",
        "risk_level": "⚠ Risk",
        "gem_status": "⭐ Status",
        "liquidity": "💵 Liquidity",
        "volume_24h": "📊 Volume",
        "fdv": "🏦 FDV"
    }
)
display_df = display_df[
    [
        "🪙 Token",
        "💰 Symbol",
        "🤖 AI",
        "💎 Gem",
        "⭐ Status",
        "⚠ Risk",
        "💵 Liquidity",
        "📊 Volume",
        "🏦 FDV"
    ]
]
st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)