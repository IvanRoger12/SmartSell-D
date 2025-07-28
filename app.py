
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SmartSell Premium Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")
    return df

df = load_data()

# Navigation
tabs = st.tabs(["📊 Dashboard", "💡 Insights & Actions"])

with tabs[0]:
    st.markdown("## 📊 SmartSell Premium Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Revenue", f"{df['Revenue'].sum():,.0f} €")
    col2.metric("⭐ Avg Rating", f"{df['Rating'].mean():.2f}/5")
    col3.metric("🎯 Success Rate", f"{df['Success'].mean()*100:.1f}%")
    col4.metric("📦 Product Count", len(df))

    st.subheader("Success Rate by Category")
    fig = px.bar(df.groupby("Category")["Success"].mean().reset_index(),
                 x="Category", y="Success", color="Category")
    st.plotly_chart(fig, use_container_width=True)

with tabs[1]:
    st.markdown("## 💡 Insights & Actions")
    top_products = df.sort_values(by=["Rating", "Sales"], ascending=False).head(10)
    st.write("🚀 High Potential Products", top_products)

    st.write("📤 Download CSV")
    st.download_button("Download", top_products.to_csv(index=False), file_name="top_products.csv")

    st.markdown("---")
    st.markdown("🔚 [My LinkedIn](https://www.linkedin.com) | 💬 Feedback: contact@example.com")
