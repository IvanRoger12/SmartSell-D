
import streamlit as st
import pandas as pd
import plotly.express as px

# --------- Fonction de traduction simple ---------
def t(en, fr):
    return fr if st.session_state.language == 'Français' else en

# --------- Configuration de la page ---------
st.set_page_config(
    page_title="SmartSell Premium Dashboard",
    layout="wide",
    page_icon="📊",
)

# --------- En-tête stylisé ---------
st.markdown("""
    <div style='background: linear-gradient(to right, #6a89cc, #8e44ad); 
                padding: 1.5rem; 
                border-radius: 1rem; 
                box-shadow: 2px 2px 15px rgba(0,0,0,0.2); 
                text-align: center;
                color: white;
                font-size: 2.5rem;
                font-weight: bold;'>
        📊 SmartSell Premium Dashboard
    </div>
    <br>
""", unsafe_allow_html=True)

# --------- Chargement des données ---------
df = pd.read_csv("ensemble de données.csv")

# --------- Initialisation de session ---------
if 'language' not in st.session_state:
    st.session_state.language = 'English'

# --------- Barre latérale ---------
st.sidebar.markdown("### 🌍 Language / Langue")
language = st.sidebar.selectbox("", ['English', 'Français'], index=0)
st.session_state.language = language

st.sidebar.markdown("## 🔍 Filters")

selected_categories = st.sidebar.multiselect(
    t("Select Categories", "Sélectionnez les catégories"),
    options=df["Category"].unique(),
    default=df["Category"].unique()[:3]
)

min_price = float(df["Price"].min())
max_price = float(df["Price"].max())

price_range = st.sidebar.slider(
    t("Price Range (€)", "Fourchette de prix (€)"),
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price)
)

rating_min = st.sidebar.slider(
    t("Minimum Rating", "Note minimale"),
    1.0, 5.0, 3.0, 0.1
)

product_query = st.sidebar.text_input("🔎 " + t("Search by Product", "Recherche par produit"))

# --------- Filtrage des données ---------
filtered_df = df[
    (df['Category'].isin(selected_categories)) &
    (df['Price'] >= price_range[0]) &
    (df['Price'] <= price_range[1]) &
    (df['Rating'] >= rating_min)
]

if product_query:
    filtered_df = filtered_df[filtered_df['App'].str.contains(product_query, case=False)]

# --------- Tabs ---------
tab1, tab2 = st.tabs([t("📊 Dashboard", "📊 Tableau de bord"), t("💡 Insights & Actions", "💡 Informations & Actions")])

with tab1:
    st.markdown("### " + t("Empowering Marketing & Sales Decisions with Intelligent Data Insights", 
                            "Optimiser les décisions marketing & ventes avec des données intelligentes"))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 " + t("Total Revenue", "Revenus Totaux"), f"{filtered_df['Revenue (Millions)'].sum():,.2f} M")
    col2.metric("⭐ " + t("Avg Rating", "Note Moyenne"), f"{filtered_df['Rating'].mean():.2f}/5")
    col3.metric("🎯 " + t("Success Rate", "Taux de Succès"), f"{filtered_df['Success Rate'].mean()*100:.1f}%")
    col4.metric("📦 " + t("Product Count", "Nombre de Produits"), f"{filtered_df.shape[0]}")

    st.markdown("### " + t("Success Rate by Category", "Taux de succès par catégorie"))
    fig = px.bar(filtered_df.groupby("Category")["Success Rate"].mean().sort_values(), orientation='h', text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### 🚀 " + t("High Potential Products", "Produits à fort potentiel"))
    high_success = filtered_df[filtered_df["Success Rate"] > 0.75]
    st.dataframe(high_success[["App", "Category", "Rating", "Price", "Success Rate"]])

    st.markdown("### 💰 " + t("Price Optimization Picks", "Optimisation des prix"))
    avg_price_per_cat = filtered_df.groupby("Category")["Price"].mean().reset_index().sort_values(by="Price")
    st.dataframe(avg_price_per_cat)

    st.markdown("### 🌞 " + t("Sunburst Chart", "Diagramme en anneau"))
    fig2 = px.sunburst(filtered_df, path=["Category", "App"], values="Success Rate")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 📈 " + t("Conversion Funnel", "Tunnel de Conversion"))
    fig3 = px.funnel(filtered_df.sort_values(by="Success Rate", ascending=False).head(5),
                     x="Success Rate", y="App")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("### 🤖 " + t("AI Insight", "Message IA"))
    median_price = filtered_df["Price"].median()
    if median_price > 500:
        st.success(t("Prices are above average, consider competitive analysis.",
                     "Les prix sont au-dessus de la moyenne, pensez à une analyse concurrentielle."))
    else:
        st.info(t("Pricing looks optimized.", "Les prix semblent optimisés."))

    st.download_button(label=t("📤 Export Report", "📤 Exporter le rapport"),
                       data=filtered_df.to_csv(index=False).encode("utf-8"),
                       file_name="smart_sell_export.csv",
                       mime="text/csv")

# --------- Signature ---------
st.markdown("---")
st.markdown("<center>© 2025 IvanRoger12 | [LinkedIn](https://linkedin.com) | Powered by Streamlit</center>", unsafe_allow_html=True)
