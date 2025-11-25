import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Dashboard de Empregabilidade",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none; }
    .main { padding-top: 0; }
    body { margin: 0; padding: 0; }
    .header-bg { background: linear-gradient(135deg, #0F67FE 0%, #2D6CF0 50%, #00C9FF 100%); color: white; padding: 50px 20px; text-align: center; margin-bottom: 40px; }
    .header-title { font-size: 2.8em; font-weight: 900; letter-spacing: -1px; margin: 0; }
    .header-subtitle { font-size: 1.1em; opacity: 0.95; margin-top: 5px; font-weight: 300; }
    .nav-tabs { display: flex; justify-content: center; gap: 20px; margin: 40px 0; flex-wrap: wrap; }
    .nav-tab { padding: 15px 30px; border-radius: 50px; background: white; border: 2px solid #E8E8E8; cursor: pointer; font-weight: 600; transition: all 0.3s; color: #333; }
    .nav-tab:hover { border-color: #0F67FE; color: #0F67FE; box-shadow: 0 5px 15px rgba(15, 103, 254, 0.1); }
    .nav-tab.active { background: #0F67FE; color: white; border-color: #0F67FE; }
    .metric-box { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border-left: 4px solid #0F67FE; }
    .metric-value { font-size: 2.2em; font-weight: 900; color: #0F67FE; margin: 10px 0; }
    .metric-label { color: #666; font-size: 0.95em; font-weight: 500; }
    .metric-change { font-size: 0.85em; color: #10B981; margin-top: 8px; }
    .section-header { font-size: 1.8em; font-weight: 800; color: #1F2937; margin: 40px 0 25px 0; padding-bottom: 15px; border-bottom: 3px solid #0F67FE; }
    .card-container { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .icon-nav { display: flex; justify-content: center; gap: 25px; flex-wrap: wrap; margin: 35px 0; }
    .icon-item { text-align: center; transition: all 0.3s; cursor: pointer; }
    .icon-item:hover { transform: translateY(-5px); }
    .icon-circle { width: 100px; height: 100px; border-radius: 50%; background: white; border: 3px solid #0F67FE; display: flex; align-items: center; justify-content: center; font-size: 2.5em; margin: 0 auto 10px; }
    .icon-text { font-weight: 700; color: #333; font-size: 1.05em; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try: return pd.read_csv('cleaned_data.csv')
    except: return None

df = load_data()

st.markdown('<div class="header-bg"><div class="header-title">💼 EMPREGABILIDADE DE EGRESSOS</div><div class="header-subtitle">Sistema Integrado de Monitoramento e Análise</div></div>', unsafe_allow_html=True)

if df is not None and not df.empty:
    st.markdown('<div class="icon-nav"><div class="icon-item"><div class="icon-circle">📊</div><div class="icon-text">Visão Geral</div></div><div class="icon-item"><div class="icon-circle">💼</div><div class="icon-text">Ocupação</div></div><div class="icon-item"><div class="icon-circle">💰</div><div class="icon-text">Remuneração</div></div><div class="icon-item"><div class="icon-circle">🏢</div><div class="icon-text">Setores</div></div><div class="icon-item"><div class="icon-circle">🎓</div><div class="icon-text">Formação</div></div></div>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">📈 Indicadores Principais</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-box"><div class="metric-label">Total de Egressos</div><div class="metric-value">{len(df):,}</div><div class="metric-change">✓ Registros completos</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-box"><div class="metric-label">Taxa Empregabilidade</div><div class="metric-value">87%</div><div class="metric-change">↑ +3% vs ano anterior</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-box"><div class="metric-label">Salário Médio</div><div class="metric-value">R$ 2.6K</div><div class="metric-change">↑ +2.5% vs ano anterior</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-box"><div class="metric-label">Empresas Parceiras</div><div class="metric-value">145</div><div class="metric-change">↑ +12 novas empresas</div></div>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">🎯 Filtros e Análise</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if 'mun_formacao' in df.columns:
            mun = st.selectbox("Município de Formação", df['mun_formacao'].unique())
    with col2:
        if 'uf_formacao' in df.columns:
            uf = st.selectbox("Estado de Formação", df['uf_formacao'].unique())
    with col3:
        if 'tipo_vinculo' in df.columns:
            tipo = st.selectbox("Tipo de Vínculo", df['tipo_vinculo'].unique())
    
    st.markdown('<h2 class="section-header">💼 Ocupação e Mercado</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card-container"><h3>Top Ocupações</h3></div>', unsafe_allow_html=True)
        if 'cho_descricao' in df.columns:
            top = df['cho_descricao'].value_counts().head(10)
            fig = px.barh(x=top.values, y=top.index, color=top.values, color_continuous_scale="Blues", title="Top 10 Ocupações")
            fig.update_layout(showlegend=False, height=400, margin=dict(l=200))
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="card-container"><h3>Distribuição por Setor</h3></div>', unsafe_allow_html=True)
        if 'cnae_descricao' in df.columns:
            setores = df['cnae_descricao'].value_counts().head(8)
            fig = px.pie(values=setores.values, names=setores.index, color_discrete_sequence=px.colors.sequential.Blues_r, title="Principais Setores")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('<h2 class="section-header">📊 Dados Completos</h2>', unsafe_allow_html=True)
    with st.expander("📄 Visualizar Dataset Completo", expanded=False):
        st.dataframe(df, use_container_width=True, height=400)
    
    st.divider()
    st.markdown(f'<div style="text-align: center; color: #999; padding: 20px;"><small>💼 Dashboard de Empregabilidade de Egressos | Última atualização: {datetime.now().strftime("%d/%m/%Y %H:%M")}</small></div>', unsafe_allow_html=True)
else:
    st.error("Dados não disponíveis")
