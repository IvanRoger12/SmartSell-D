
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import base64

# Configuration page
st.set_page_config(page_title="📊 SmartSell Premium Dashboard", layout="wide")

# Sidebar - Langue
langue = st.sidebar.selectbox("🌍 Choisissez la langue / Select Language", ["Français", "English"])

# Traduction rapide
def t(fr, en):
    return fr if langue == "Français" else en

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")
    return df

df = load_data()

# Filtres
st.sidebar.header(t("🎛️ Filtres", "🎛️ Filters"))
selected_categories = st.sidebar.multiselect(t("Catégories", "Categories"), df["Category"].unique(), default=df["Category"].unique())
price_range = st.sidebar.slider(t("Prix (€)", "Price (€)"), int(df["Price"].min()), int(df["Price"].max()), (int(df["Price"].min()), int(df["Price"].max())))
rating_filter = st.sidebar.slider(t("Note minimale", "Minimum Rating"), 1.0, 5.0, 3.0, step=0.1)

# Filtrage
filtered_df = df[
    (df["Category"].isin(selected_categories)) &
    (df["Price"].between(price_range[0], price_range[1])) &
    (df["Rating"] >= rating_filter)
]

# Navigation entre onglets
page = st.selectbox("", [t("📊 Dashboard", "📊 Dashboard"), t("💡 Insights & Actions", "💡 Insights & Actions")])

if page == t("📊 Dashboard", "📊 Dashboard"):
    st.markdown(f"<h1 style='text-align:center;'>{t('📊 Dashboard', '📊 Dashboard')}</h1>", unsafe_allow_html=True)

    # KPI
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 " + t("Revenu Total", "Total Revenue"), f"{(filtered_df['Price'] * filtered_df['Sales_y']).sum():,.0f} €")
    with col2:
        st.metric("⭐ " + t("Note Moyenne", "Average Rating"), f"{filtered_df['Rating'].mean():.2f}/5")
    with col3:
        st.metric("🎯 " + t("Taux de Succès", "Success Rate"), f"{filtered_df['Success_Percentage'].mean():.1f}%")
    with col4:
        st.metric("📦 " + t("Produits", "Products"), f"{len(filtered_df)}")

    # Graphiques
    st.plotly_chart(
        px.bar(
            filtered_df.groupby("Category")["Success_Percentage"].mean().reset_index(),
            x="Category",
            y="Success_Percentage",
            color="Category",
            title=t("Taux de succès par catégorie", "Success Rate by Category")
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.scatter(
            filtered_df,
            x="Price",
            y="Success_Percentage",
            size="Sales_y",
            color="Rating",
            hover_data=["Product_Name"],
            title=t("Analyse Prix vs Succès", "Price vs Success Analysis")
        ),
        use_container_width=True
    )

    # Courbe de tendance
    st.plotly_chart(
        px.line(
            filtered_df.assign(Year=[datetime.now().year - i % 5 for i in range(len(filtered_df))])
            .groupby("Year")["Success_Percentage"].mean().reset_index(),
            x="Year",
            y="Success_Percentage",
            title=t("📈 Courbe de Tendance", "📈 Trend Curve")
        ),
        use_container_width=True
    )

elif page == t("💡 Insights & Actions", "💡 Insights & Actions"):
    st.markdown(f"<h1 style='text-align:center;'>{t('💡 Insights & Actions', '💡 Insights & Actions')}</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🚀 " + t("Produits à haut potentiel", "High Potential Products"))
        top = filtered_df.sort_values(by=["Rating", "Sales_y"], ascending=False).head(10)
        st.dataframe(top[["Product_Name", "Price", "Rating", "Sales_y"]])

    with col2:
        st.subheader("💰 " + t("Produits à Optimiser", "Price Optimization Picks"))
        low_perf = filtered_df[filtered_df["Success_Percentage"] < 30].sort_values(by="Price", ascending=False).head(10)
        st.dataframe(low_perf[["Product_Name", "Price", "Success_Percentage"]])

    # IA Insight
    st.subheader("🤖 " + t("Analyse IA", "AI Insight"))
    median_price = df["Price"].median()
    mean_price = filtered_df["Price"].mean()
    if mean_price > median_price:
        st.info(t("💡 Les prix sont globalement élevés, envisagez une stratégie de baisse sélective.", 
                  "💡 Prices are relatively high, consider a selective price drop strategy."))
    else:
        st.success(t("✅ Les prix sont bien alignés avec la médiane du marché.", 
                     "✅ Prices are aligned with market median."))

    # Sunburst
    st.subheader("🌞 " + t("Exploration par catégorie", "Category Exploration"))
    if "Sub_Category" in df.columns:
        st.plotly_chart(
            px.sunburst(df, path=["Category", "Sub_Category"], values="Sales_y", color="Success_Percentage"),
            use_container_width=True
        )

    # Funnel Chart simple (catégories fictives)
    st.subheader("📈 " + t("Funnel de conversion", "Conversion Funnel"))
    funnel_data = pd.DataFrame({
        "Étape": ["Visites", "Consultations", "Ajouts Panier", "Commandes", "Livraisons"],
        "Volume": [10000, 8000, 3000, 1200, 900]
    })
    st.plotly_chart(
        px.funnel(funnel_data, x="Volume", y="Étape", title=t("Parcours Client", "Customer Journey")),
        use_container_width=True
    )

    # Export Excel
    st.subheader("📤 " + t("Exporter les données", "Export Report"))
    def convert_df_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Filtered")
        return output.getvalue()

    excel_data = convert_df_to_excel(filtered_df)
    b64 = base64.b64encode(excel_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="SmartSell_Report.xlsx">{t("📥 Télécharger Excel", "📥 Download Excel")}</a>'
    st.markdown(href, unsafe_allow_html=True)

    # Feedback et signature
    st.markdown("---")
    st.markdown(f"**🔚 SmartSell by Ivan** | [💼 LinkedIn](https://www.linkedin.com/in/ivanroger12)")

    st.text_area(t("💬 Laissez un feedback ici", "💬 Leave feedback here"))
