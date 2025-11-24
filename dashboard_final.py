import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard de Empregabilidade - Versão Visual",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Estilo e Cores Vibrantes (Tema Claro/Contraste) ---
PRIMARY_COLOR = "#007ACC"  # Azul Vibrante
SECONDARY_COLOR = "#FF4ABB"  # Vermelho/Laranja para Destaque
COLOR_SEQUENCE = px.colors.qualitative.Vivid  # Sequencia de cores vibrantes

# --- Carregamento e Cache de Dados ---
@st.cache_data
def load_data():
    """Carrega os dados limpsos limbos."""
    try:
        df = pd.read_csv('cleaned_data.csv')
        return df
    except:
        st.error('Erro ao carregar dados limpos')
        return None

def main():
    st.title('Dashboard de Empregabilidade - Versão Visual')
    st.markdown('---')
    
    # Carregar dados
    df = load_data()
    
    if df is None or df.empty:
        st.warning('Nenhum dado disponível. Verifique se o arquivo cleaned_data.csv existe.')
        return
    
    # Sidebar - Filtros
    st.sidebar.header('Filtros')
    
    # Mostrar algumas métricas básicas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Total de Registros', len(df))
    with col2:
        st.metric('Colunas', len(df.columns))
    with col3:
        st.metric('Última Atualização', 'Hoje')
    
    st.markdown('---')
    
    # Exibir primeiras linhas dos dados
    st.subheader('Prévia dos Dados')
    st.dataframe(df.head(10), use_container_width=True)
    
    # Estatísticas descritivas
    if st.checkbox('Mostrar Estatísticas Descritivas'):
        st.subheader('Estatísticas Descritivas')
        st.write(df.describe())

if __name__ == '__main__':
    main()
