
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime

# Langues supportées
languages = {
    "fr": {
        "title": "📊 Tableau de Bord SmartSell Premium",
        "revenue": "💰 Revenu Total",
        "avg_rating": "⭐ Note Moyenne",
        "success_rate": "🎯 Taux de Succès",
        "product_count": "📦 Nombre de Produits",
        "select_language": "🌐 Sélectionnez la langue",
        "filters": "🎛️ Filtres",
        "category": "Catégories",
        "price_range": "Plage de prix (€)",
        "rating": "Note minimale",
        "product_search": "🔍 Rechercher un produit",
        "dashboard": "📊 Tableau de bord",
        "insights": "💡 Analyses & Actions",
        "sunburst": "🌞 Diagramme Sunburst",
        "funnel": "📈 Tunnel de conversion",
        "ai_insight": "🤖 Analyse IA basée sur le prix médian",
        "export_excel": "📤 Exporter Excel",
        "raw_data": "📄 Voir les données brutes",
        "linkedin": "🔗 Mon profil LinkedIn",
        "feedback": "💬 Laisser un commentaire"
    },
    "en": {
        "title": "📊 SmartSell Premium Dashboard",
        "revenue": "💰 Total Revenue",
        "avg_rating": "⭐ Average Rating",
        "success_rate": "🎯 Success Rate",
        "product_count": "📦 Product Count",
        "select_language": "🌐 Select Language",
        "filters": "🎛️ Filters",
        "category": "Categories",
        "price_range": "Price Range (€)",
        "rating": "Minimum Rating",
        "product_search": "🔍 Search Product",
        "dashboard": "📊 Dashboard",
        "insights": "💡 Insights & Actions",
        "sunburst": "🌞 Sunburst Chart",
        "funnel": "📈 Funnel Chart",
        "ai_insight": "🤖 AI Insight Based on Median Price",
        "export_excel": "📤 Export Excel",
        "raw_data": "📄 View Raw Data",
        "linkedin": "🔗 My LinkedIn",
        "feedback": "💬 Leave Feedback"
    },
    "es": {
        "title": "📊 Panel Premium SmartSell",
        "revenue": "💰 Ingresos Totales",
        "avg_rating": "⭐ Calificación Promedio",
        "success_rate": "🎯 Tasa de Éxito",
        "product_count": "📦 Cantidad de Productos",
        "select_language": "🌐 Seleccionar idioma",
        "filters": "🎛️ Filtros",
        "category": "Categorías",
        "price_range": "Rango de Precios (€)",
        "rating": "Calificación mínima",
        "product_search": "🔍 Buscar producto",
        "dashboard": "📊 Panel",
        "insights": "💡 Análisis y Acciones",
        "sunburst": "🌞 Gráfico Sunburst",
        "funnel": "📈 Gráfico de embudo",
        "ai_insight": "🤖 Análisis de IA basado en el precio medio",
        "export_excel": "📤 Exportar a Excel",
        "raw_data": "📄 Ver datos sin procesar",
        "linkedin": "🔗 Mi LinkedIn",
        "feedback": "💬 Dejar un comentario"
    },
    "it": {
        "title": "📊 Cruscotto SmartSell Premium",
        "revenue": "💰 Entrate Totali",
        "avg_rating": "⭐ Valutazione Media",
        "success_rate": "🎯 Tasso di Successo",
        "product_count": "📦 Numero di Prodotti",
        "select_language": "🌐 Seleziona lingua",
        "filters": "🎛️ Filtri",
        "category": "Categorie",
        "price_range": "Fascia di Prezzo (€)",
        "rating": "Valutazione minima",
        "product_search": "🔍 Cerca prodotto",
        "dashboard": "📊 Cruscotto",
        "insights": "💡 Approfondimenti e Azioni",
        "sunburst": "🌞 Grafico Sunburst",
        "funnel": "📈 Grafico a imbuto",
        "ai_insight": "🤖 Analisi AI basata sul prezzo medio",
        "export_excel": "📤 Esporta Excel",
        "raw_data": "📄 Visualizza dati grezzi",
        "linkedin": "🔗 Il mio LinkedIn",
        "feedback": "💬 Lascia un commento"
    },
    "zh": {
        "title": "📊 SmartSell 高级仪表板",
        "revenue": "💰 总收入",
        "avg_rating": "⭐ 平均评分",
        "success_rate": "🎯 成功率",
        "product_count": "📦 产品总数",
        "select_language": "🌐 选择语言",
        "filters": "🎛️ 筛选器",
        "category": "类别",
        "price_range": "价格范围 (€)",
        "rating": "最低评分",
        "product_search": "🔍 搜索产品",
        "dashboard": "📊 仪表板",
        "insights": "💡 洞察与行动",
        "sunburst": "🌞 旭日图",
        "funnel": "📈 漏斗图",
        "ai_insight": "🤖 基于中位数价格的AI洞察",
        "export_excel": "📤 导出Excel",
        "raw_data": "📄 查看原始数据",
        "linkedin": "🔗 我的LinkedIn",
        "feedback": "💬 留下反馈"
    }
}

# Sélection de la langue
lang_code = st.sidebar.selectbox("🌐 Lang / Language", options=list(languages.keys()), format_func=lambda x: x.upper())
t = languages[lang_code]

# Exemple d'affichage
st.title(t["title"])
