
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from PIL import Image
import base64

# Dataset
df = pd.read_csv("dataset.csv")
df['Revenue'] = df['Price'] * df['Sales_m']

# Thème
st.set_page_config(page_title="SmartSell Premium Dashboard", layout="wide")

# Mode clair/sombre auto
theme_toggle = st.sidebar.radio("🌓 Theme", ["🌞 Light", "🌙 Dark"])
st.markdown(f"<style>body {{ background-color: {'#fff' if theme_toggle == '🌞 Light' else '#222'}; color: {'#000' if theme_toggle == '🌞 Light' else '#fff'}; }}</style>", unsafe_allow_html=True)

# Header
st.markdown("""
<div style='text-align: center; padding: 1rem; border-radius: 20px; background: linear-gradient(to right, #6a89cc, #8e44ad); color: white; box-shadow: 0px 4px 12px rgba(0,0,0,0.2);'>
    <h1>📊 SmartSell Premium Dashboard</h1>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["📊 Dashboard", "💡 Insights & Actions"])

with tab1:
    st.subheader("📌 Aperçu global")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Revenue", f"{df['Revenue'].sum():,.0f} €")
    col2.metric("⭐ Note Moyenne", f"{df['Rating'].mean():.2f}/5")
    col3.metric("🎯 Taux de Succès", f"{df['Success_Percentage'].mean():.1f}%")
    col4.metric("📦 Nombre de Produits", df.shape[0])

    # Filtres
    st.sidebar.subheader("🎛️ Filtres")
    categories = st.sidebar.multiselect("Catégories", df["Category"].unique(), default=df["Category"].unique())
    price_range = st.sidebar.slider("Plage de Prix (€)", float(df["Price"].min()), float(df["Price"].max()), (float(df["Price"].min()), float(df["Price"].max())))
    min_rating = st.sidebar.slider("Note minimale", 1.0, 5.0, 3.0)
    search_term = st.sidebar.text_input("🔍 Recherche produit")

    filtered_df = df[
        (df["Category"].isin(categories)) &
        (df["Price"].between(price_range[0], price_range[1])) &
        (df["Rating"] >= min_rating)
    ]

    if search_term:
        filtered_df = filtered_df[filtered_df["Product_Name"].str.contains(search_term, case=False)]

    # Graphiques
    st.subheader("📈 Taux de Succès par Catégorie")
    bar_fig = px.bar(filtered_df.groupby("Category")["Success_Percentage"].mean().reset_index(),
                     x="Category", y="Success_Percentage", color="Category")
    st.plotly_chart(bar_fig, use_container_width=True)

    st.subheader("🌞 Répartition par Catégorie/Sous-catégorie (Sunburst)")
    sunburst = px.sunburst(filtered_df, path=['Category', 'Sub_category'], values='Revenue')
    st.plotly_chart(sunburst, use_container_width=True)

    st.subheader("📈 Funnel de Conversion (Basé sur ventes)")
    funnel_df = filtered_df.groupby("Category")[["Sales_m"]].sum().sort_values("Sales_m", ascending=False).reset_index()
    funnel_fig = px.funnel(funnel_df, x="Sales_m", y="Category")
    st.plotly_chart(funnel_fig, use_container_width=True)

with tab2:
    st.subheader("🚀 Produits à Haut Potentiel")
    high_potential = filtered_df[(filtered_df["Rating"] >= 4.0) & (filtered_df["Sales_m"] > filtered_df["Sales_m"].median())]
    st.dataframe(high_potential[["Product_Name", "Price", "Rating", "Sales_m"]])

    st.subheader("💰 Produits à Optimiser (Prix > Médiane)")
    price_median = filtered_df["Price"].median()
    overpriced = filtered_df[filtered_df["Price"] > price_median]
    st.dataframe(overpriced[["Product_Name", "Price", "Rating", "Sales_m"]])

    st.subheader("🤖 Insight IA Automatisé")
    if df["Price"].mean() > price_median:
        st.success("💡 Astuce IA : Le prix moyen des produits dépasse la médiane. Envisagez une optimisation tarifaire !")
    else:
        st.info("📉 Les prix sont globalement équilibrés par rapport à la médiane.")

    # Export
    st.subheader("📤 Exporter les données")
    @st.cache_data
    def convert_df_to_csv(dataframe):
        return dataframe.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Télécharger les données filtrées (CSV)",
        data=convert_df_to_csv(filtered_df),
        file_name='smart_data_export.csv',
        mime='text/csv'
    )

    st.subheader("📄 Données brutes")
    st.dataframe(filtered_df)

    st.markdown("---")
    st.markdown("🔚 [Créé par IvanRoger12](https://www.linkedin.com/in/ivanroger12) • 💬 Vos retours sont les bienvenus !")
