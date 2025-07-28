
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# Chargement des données
df = pd.read_csv("dataset.csv")

# Calcul revenu si la colonne n'existe pas
if 'Revenue' not in df.columns:
    df['Revenue'] = df['Price'] * df['Sales_y']

# Config page
st.set_page_config(page_title="SmartSell Premium", layout="wide")

# Titre centré
st.markdown("<h1 style='text-align: center;'>📊 SmartSell Premium Dashboard</h1>", unsafe_allow_html=True)

# Sélecteur de langue
langue = st.selectbox("🌐 Choisir la langue", ["Français", "English"])

# KPI
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Revenue", f"{df['Revenue'].sum():,.0f} €")
col2.metric("⭐ Note moyenne", f"{df['Rating'].mean():.2f}/5")
col3.metric("🎯 Taux de succès", f"{df['Success_Percentage'].mean():.2f}%")
col4.metric("📦 Nombre de produits", str(len(df)))

# Courbe de tendance simulée
st.subheader("📈 Tendance de Revenu")
trend_data = df.groupby(df.index // 30).agg({'Revenue': 'sum'})
fig_trend = px.line(trend_data, y="Revenue", title="Courbe de tendance")
st.plotly_chart(fig_trend, use_container_width=True)

# Sunburst chart
st.subheader("🌞 Répartition des produits")
fig_sunburst = px.sunburst(df, path=['Category', 'Product_Name'], values='Sales_y')
st.plotly_chart(fig_sunburst, use_container_width=True)

# Funnel Chart
st.subheader("📉 Funnel de Conversion")
funnel_data = pd.DataFrame({
    "Étape": ["Visites", "Ajouts au panier", "Commandes", "Achats"],
    "Valeur": [100000, 60000, 30000, 15000]
})
fig_funnel = go.Figure(go.Funnel(
    y=funnel_data["Étape"],
    x=funnel_data["Valeur"]
))
st.plotly_chart(fig_funnel, use_container_width=True)

# IA message conditionnel
st.subheader("🤖 Insight IA")
median_price = df['Price'].median()
mean_price = df['Price'].mean()
if mean_price > median_price:
    st.success("💡 Les prix moyens sont au-dessus de la médiane. Envisagez des ajustements stratégiques.")
else:
    st.info("✅ Les prix sont bien alignés avec le marché.")

# Export Excel
st.subheader("📤 Exporter les données")
@st.cache_data
def convert_df_to_excel(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        dataframe.to_excel(writer, index=False, sheet_name='Produits')
    return output.getvalue()

excel = convert_df_to_excel(df)
st.download_button(label="📥 Télécharger Excel", data=excel, file_name="smartsell_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Signature
st.markdown("---")
st.markdown("🔗 [Me contacter sur LinkedIn](https://www.linkedin.com/in/tonprofil)", unsafe_allow_html=True)
st.text_area("💬 Feedback")

