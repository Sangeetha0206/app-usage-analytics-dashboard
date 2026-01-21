
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import time

# ---------------------
# Page Config + Theme
# ---------------------
st.set_page_config(
    page_title="App Usage Dashboard",
    page_icon="📊",
    layout="wide"
)

plt.style.use("seaborn-v0_8-darkgrid")

# ---------------------
# Loading Animation
# ---------------------
with st.spinner("🚀 Loading Dashboard..."):
    time.sleep(1)
st.success("Dashboard Loaded Successfully ✅")

# ---------------------
# Load Data
# ---------------------
dau = pd.read_csv("app_usage.csv", parse_dates=["date"])
df = pd.read_csv("app_usage_data.csv", parse_dates=["date"])

# ---------------------
# Title
# ---------------------
st.title("📊 App Usage Analytics Dashboard")
st.markdown("Analyze **Daily Active Users, Retention & Feature Usage**")

st.markdown("---")

# ---------------------
# Date Filter
# ---------------------
min_date = df["date"].min()
max_date = df["date"].max()

start_date, end_date = st.date_input(
    "📅 Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

filtered_df = df[
    (df["date"] >= pd.to_datetime(start_date)) &
    (df["date"] <= pd.to_datetime(end_date))
]

# ---------------------
# Retention Calculation
# ---------------------
retention = dau.copy()
retention["Retention Rate"] = (
    retention["Daily Active Users"] /
    retention["Daily Active Users"].iloc[0]
) * 100

# ---------------------
# Summary Metrics (Animated Feel)
# ---------------------
total_users = filtered_df["user_id"].nunique()
avg_retention = round(retention["Retention Rate"].mean(), 2)
total_sessions = len(filtered_df)

c1, c2, c3 = st.columns(3)
c1.metric("👥 Total Users", total_users, delta="+10%")
c2.metric("🔁 Avg Retention (%)", avg_retention, delta="+3%")
c3.metric("📌 Total Sessions", total_sessions, delta="+25")

st.markdown("---")

# ---------------------
# Interactive Charts (PLOTLY)
# ---------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Daily Active Users")
    fig_dau = px.line(
        dau,
        x="date",
        y="Daily Active Users",
        markers=True,
        title="Daily Active Users Trend"
    )
    st.plotly_chart(fig_dau, use_container_width=True)

with col2:
    st.subheader("🔁 Retention Rate")
    fig_ret = px.line(
        retention,
        x="date",
        y="Retention Rate",
        markers=True,
        title="User Retention Trend"
    )
    st.plotly_chart(fig_ret, use_container_width=True)

st.markdown("---")

# ---------------------
# Feature Usage
# ---------------------
st.subheader("🚀 Feature Usage Insights")

feature_usage = filtered_df["feature"].value_counts().reset_index()
feature_usage.columns = ["Feature", "Usage Count"]

# Highlight Top Feature
top_feature = feature_usage.iloc[0]["Feature"]
st.success(f"🔥 Most Used Feature: **{top_feature}**")

col3, col4 = st.columns(2)

with col3:
    st.dataframe(feature_usage)

with col4:
    fig_feat = px.bar(
        feature_usage,
        x="Feature",
        y="Usage Count",
        title="Feature Usage Count",
        color="Usage Count"
    )
    st.plotly_chart(fig_feat, use_container_width=True)

st.markdown("---")

# ---------------------
# Download Button
# ---------------------
st.download_button(
    "⬇ Download Feature Usage Data",
    feature_usage.to_csv(index=False),
    "feature_usage.csv",
    "text/csv"
)

# ---------------------
# Footer
# ---------------------
st.markdown(
    "<center>💡 Built with Streamlit | App Usage Analytics Project</center>",
    unsafe_allow_html=True
)

