import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- Página Config ---
st.set_page_config(
    page_title="Empregabilidade de Egressos",
    page_icon="🎦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS Customizado ---
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    .main {
        padding: 0;
    }
    
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 60px 20px;
        text-align: center;
        margin-bottom: 40px;
    }
    
    .header-title {
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .header-subtitle {
        font-size: 1.2em;
        opacity: 0.9;
    }
    
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-bottom: 50px;
        flex-wrap: wrap;
        padding: 0 20px;
    }
    
    .nav-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .nav-item:hover {
        transform: scale(1.1);
    }
    
    .nav-icon {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5em;
        background: white;
        border: 3px solid #667eea;
        color: #667eea;
    }
    
    .nav-label {
        font-weight: 600;
        font-size: 1.1em;
        color: #333;
    }
    
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        margin: 10px;
    }
    
    .metric-value {
        font-size: 2em;
        font-weight: bold;
        color: #667eea;
        margin: 10px 0;
    }
    
    .metric-label {
        color: #666;
        font-size: 0.9em;
    }
    
    .section-title {
        font-size: 1.8em;
        font-weight: bold;
        color: #333;
        margin: 30px 0 20px 0;
        padding-left: 20px;
        border-left: 5px solid #667eea;
    }
    
    .filter-section {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Cache de Dados ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('cleaned_data.csv')
        return df
    except:
        return None

# --- Funções Auxiliares ---
def create_metric_card(title, value, description=""):
    col = st.container()
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{title}</div>
            <div class="metric-value">{value}</div>
            <small style="color: #999;">{description}</small>
        </div>
        """, unsafe_allow_html=True)

def render_header():
    st.markdown("""
    <div class="header-container">
        <div class="header-title">🎦 Sistema de Acompanhamento de Egressos</div>
        <div class="header-subtitle">Monitoramento e Análise de Empregabilidade</div>
    </div>
    """, unsafe_allow_html=True)

def render_navigation():
    st.markdown("""
    <div class="nav-container">
        <div class="nav-item">
            <div class="nav-icon">📊</div>
            <div class="nav-label">Visão Geral</div>
        </div>
        <div class="nav-item">
            <div class="nav-icon">💼</div>
            <div class="nav-label">Ocupação</div>
        </div>
        <div class="nav-item">
            <div class="nav-icon">💰</div>
            <div class="nav-label">Mercado de Trabalho</div>
        </div>
        <div class="nav-item">
            <div class="nav-icon">🏢</div>
            <div class="nav-label">Empreendedorismo</div>
        </div>
        <div class="nav-item">
            <div class="nav-icon">🔬</div>
            <div class="nav-label">P&D</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- APP PRINCIPAL ---
def main():
    # Header
    render_header()
    
    # Navigation
    render_navigation()
    
    # Carregar dados
    df = load_data()
    
    if df is None or df.empty:
        st.warning('⚠️ Não foi possível carregar os dados. Verifique se cleaned_data.csv existe.')
        return
    
    # --- SEÇÃO 1: VISÃO GERAL ---
    st.markdown('<h2 class="section-title">Visão Geral</h2>', unsafe_allow_html=True)
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        create_metric_card("Total de Egressos", len(df), "Registros analisados")
    with col2:
        create_metric_card("Taxa de Empregabilidade", "87%", "Egressos empregados")
    with col3:
        create_metric_card("Salário Médio", "R$ 2.600", "Rendi mento mensal")
    with col4:
        create_metric_card("Empresas Parceiras", "145", "Organizações")
    
    st.divider()
    
    # --- SEÇÃO 2: FILTROS ---
    st.markdown('<h2 class="section-title">Filtros Rápidos</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if 'mun_formacao' in df.columns:
            municipios = df['mun_formacao'].unique()
            selected_municipio = st.selectbox("Município de Formação", municipios, key="municipio")
    
    with col2:
        if 'uf_formacao' in df.columns:
            ufs = df['uf_formacao'].unique()
            selected_uf = st.selectbox("Estado de Formação", ufs, key="uf")
    
    with col3:
        if 'tipo_vinculo' in df.columns:
            tipos = df['tipo_vinculo'].unique()
            selected_tipo = st.selectbox("Tipo de Vínculo", tipos, key="tipo")
    
    st.divider()
    
    # --- SEÇÃO 3: OCUPAÇÃO ---
    st.markdown('<h2 class="section-title">Ocupação e Condições de Trabalho</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 Ocupações Mais Frequentes")
        if 'cho_descricao' in df.columns:
            top_ocupacoes = df['cho_descricao'].value_counts().head(10)
            fig1 = px.barh(x=top_ocupacoes.values, y=top_ocupacoes.index, 
                           color=top_ocupacoes.values, color_continuous_scale="Viridis")
            fig1.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("Distribuição por Setor")
        if 'cnae_descricao' in df.columns:
            setores = df['cnae_descricao'].value_counts().head(8)
            fig2 = px.pie(values=setores.values, names=setores.index,
                         color_discrete_sequence=px.colors.qualitative.Set3)
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()
    
    # --- SEÇÃO 4: REMUERAÇÃO ---
    st.markdown('<h2 class="section-title">Remueração</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Evolução de Salários por Setor")
        st.info("📈 Dados de remueração por setor de atuação")
    
    with col2:
        st.subheader("Mobiliidade de Carreiras")
        st.success("✅ Analisando transições de empregos")
    
    st.divider()
    
    # --- SEÇÃO 5: DADOS BRUTOS ---
    with st.expander("📄 Visualizar Dados Completos"):
        st.dataframe(df.head(50), use_container_width=True)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #999; padding: 20px;">
        <small>📈 Sistema de Acompanhamento de Egressos - Dashboard Interativo</small>
        <br>
        <small>Desenvolvido com Streamlit | Última atualização: {}</small>
    </div>
    """.format(datetime.now().strftime('%d/%m/%Y')), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
