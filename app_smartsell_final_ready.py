
# ===============================
# 📊 SmartSell Premium Dashboard
# Final Version — Optimized
# ===============================

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from io import BytesIO
import base64

# ====================
# 🌍 Choix de la langue
# ====================
lang = st.sidebar.selectbox("🌐 Langue / Language", ["Français", "English"])

# Texte multilingue
def t(fr, en):
    return fr if lang == "Français" else en

# ================
# 📥 Chargement data
# ================
@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")
    df['Revenue'] = df['Price'] * df['Sales_y']
    df['Year'] = [datetime.now().year - i % 5 for i in range(len(df))]
    return df

df = load_data()

# =========================
# 🔍 Barre latérale (Filtres)
# =========================
st.sidebar.title("🎛️ " + t("Filtres", "Filters"))

# Recherche de produit
search_query = st.sidebar.text_input("🔎 " + t("Rechercher un produit", "Search product"))

# Filtres classiques
categories = st.sidebar.multiselect(t("Catégories", "Categories"), options=df["Category"].unique(), default=df["Category"].unique())
price_range = st.sidebar.slider(t("Plage de prix (€)", "Price range (€)"), int(df["Price"].min()), int(df["Price"].max()), (100, 1000))
min_rating = st.sidebar.slider(t("Note minimale", "Min rating"), 1.0, 5.0, 3.0, step=0.1)

# Filtrage
filtered_df = df[
    (df['Category'].isin(categories)) &
    (df['Price'].between(price_range[0], price_range[1])) &
    (df['Rating'] >= min_rating)
]
if search_query:
    filtered_df = filtered_df[filtered_df["Product_Name"].str.contains(search_query, case=False)]

# =======================
# ⏹️ Mise en page principale
# =======================
tab1, tab2 = st.tabs(["📊 Dashboard", "💡 Insights & Actions"])

with tab1:
    st.title("🚀 SmartSell Premium Dashboard")
    st.markdown(t("**Analyse des performances produits**", "**Product performance overview**"))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 " + t("Revenu total", "Total Revenue"), f"{filtered_df['Revenue'].sum():,.0f} €")
    col2.metric("⭐ " + t("Note moyenne", "Average Rating"), f"{filtered_df['Rating'].mean():.2f}")
    col3.metric("🎯 " + t("Taux de succès", "Success Rate"), f"{filtered_df['Success_Percentage'].mean():.1f}%")
    col4.metric("📦 " + t("Nombre de produits", "Product Count"), f"{len(filtered_df)}")

    # Barres par catégorie
    fig1 = px.bar(
        filtered_df.groupby("Category").agg({"Success_Percentage": "mean"}).reset_index(),
        x="Category", y="Success_Percentage", title=t("Taux de succès par catégorie", "Success Rate by Category"),
        color="Category"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Scatter
    fig2 = px.scatter(
        filtered_df, x="Price", y="Success_Percentage", color="Rating", size="Sales_y",
        hover_name="Product_Name", title=t("Prix vs Taux de succès", "Price vs Success Rate")
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Tendance
    trend = filtered_df.groupby("Year")["Revenue"].sum().reset_index()
    fig3 = px.line(trend, x="Year", y="Revenue", title=t("Tendance de revenu dans le temps", "Revenue Trend Over Time"))
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    st.subheader("🚀 " + t("Produits à fort potentiel", "High Potential Products"))
    top_df = filtered_df.sort_values(by=["Rating", "Sales_y"], ascending=False).head(10)
    st.dataframe(top_df[["Product_Name", "Price", "Rating", "Success_Percentage"]], use_container_width=True)

    st.subheader("💰 " + t("Produits à optimiser", "Price Optimization Picks"))
    low_perf = filtered_df[filtered_df["Success_Percentage"] < 40].nlargest(5, "Price")
    st.dataframe(low_perf[["Product_Name", "Price", "Success_Percentage"]], use_container_width=True)

    st.subheader("🤖 " + t("Insight IA", "AI-Based Insight"))
    median_price = df["Price"].median()
    mean_price = filtered_df["Price"].mean()
    if mean_price > median_price:
        st.info(t("💡 Le prix moyen dépasse la médiane — envisagez une réduction pour améliorer la conversion.",
                  "💡 The average price exceeds the median — consider lowering prices to improve conversion."))
    else:
        st.success(t("✅ Les prix sont globalement compétitifs.", "✅ Prices are generally competitive."))

    # Sunburst Chart
    st.subheader("🌞 " + t("Répartition par catégorie", "Category Breakdown"))
    fig4 = px.sunburst(filtered_df, path=["Category", "Product_Name"], values="Sales_y")
    st.plotly_chart(fig4, use_container_width=True)

    # Funnel Chart simulé
    st.subheader("📈 " + t("Funnel de conversion", "Conversion Funnel"))
    st.markdown(t("Étapes simulées : Visites ➝ Ajouts panier ➝ Achats", "Simulated steps: Visits ➝ Cart ➝ Purchases"))
    funnel_df = pd.DataFrame({
        "Step": ["Visites", "Ajouts au panier", "Achats"],
        "Users": [100000, 30000, 7500]
    })
    fig5 = px.funnel(funnel_df, x="Users", y="Step")
    st.plotly_chart(fig5, use_container_width=True)

    # Export
    st.subheader("📤 " + t("Exporter", "Export"))
    def convert_df_to_excel(data):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            data.to_excel(writer, index=False)
        return output.getvalue()

    excel = convert_df_to_excel(filtered_df)
    b64 = base64.b64encode(excel).decode()
    st.markdown(f'<a href="data:application/octet-stream;base64,{b64}" download="filtered_data.xlsx">📥 {t("Télécharger Excel", "Download Excel")}</a>', unsafe_allow_html=True)

    # Feedback
    st.markdown("---")
    st.markdown("💬 " + t("Votre avis nous intéresse !", "We value your feedback!") + " 👉 [LinkedIn](https://linkedin.com)")
