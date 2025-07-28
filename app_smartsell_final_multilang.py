
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Détection de la langue
lang = st.sidebar.selectbox("🌍 Choisir la langue", ["Français", "English", "Español", "Italiano", "中文"])

# Traductions simples (pour la démo)
def t(fr, en, es, it, zh):
    if lang == "Français":
        return fr
    elif lang == "English":
        return en
    elif lang == "Español":
        return es
    elif lang == "Italiano":
        return it
    elif lang == "中文":
        return zh

# Titre de l'application
st.title(t("📊 Tableau de bord SmartSell", "📊 SmartSell Dashboard", "📊 Panel de SmartSell", "📊 Cruscotto SmartSell", "📊 SmartSell 数据面板"))

# Chargement des données
df = pd.read_csv("dataset.csv")

# Filtres simples
st.sidebar.markdown("### " + t("Filtres", "Filters", "Filtros", "Filtri", "筛选条件"))
selected_categories = st.sidebar.multiselect(t("Catégories", "Categories", "Categorías", "Categorie", "类别"), df['Category'].unique())
filtered_df = df[df['Category'].isin(selected_categories)] if selected_categories else df

# KPI
st.metric(t("💰 Revenu total", "💰 Total Revenue", "💰 Ingreso total", "💰 Entrate totali", "💰 总收入"), f"{(filtered_df['Price'] * filtered_df['Sales_y']).sum():,.0f} €")
