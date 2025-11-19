import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard de Empregabilidade - Versão Visual",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Estilo e Cores Vibrantes (Tema Claro/Contraste) ---
PRIMARY_COLOR = "#007ACC" # Azul Vibrante
SECONDARY_COLOR = "#FF4B4B" # Vermelho/Laranja para Destaque
COLOR_SEQUENCE = px.colors.qualitative.Vivid # Sequência de cores vibrantes

# --- Carregamento e Cache de Dados ---
@st.cache_data
def load_data():
    """Carrega os dados limpos."""
    try:
        df = pd.read_csv("cleaned_data.csv")
        # Conversão de tipos para garantir
        df['remun_media_nominal'] = pd.to_numeric(df['remun_media_nominal'], errors='coerce')
        df['tempo_emprego_meses'] = pd.to_numeric(df['tempo_emprego_meses'], errors='coerce')
        df['carga_horaria'] = pd.to_numeric(df['carga_horaria'], errors='coerce')
        df['ano_admissao'] = df['ano_admissao'].astype('Int64')
        df['data_admissao'] = pd.to_datetime(df['mes_ano_admissao'])
        return df
    except FileNotFoundError:
        st.error("Arquivo de dados 'cleaned_data.csv' não encontrado. Execute 'data_processor.py' primeiro.")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# --- Título e Introdução ---
st.title("✨ Painel Visual de Empregabilidade de Egressos")
st.markdown("""
Esta versão foca na **experiência intuitiva** e na **compreensão imediata** dos dados, utilizando cores vibrantes e um layout dinâmico.
""")

# --- Sidebar para Filtros (Simplificados) ---
st.sidebar.header("Filtros Rápidos")

# Filtro de Ano de Admissão
min_year = int(df['ano_admissao'].min()) if not df['ano_admissao'].empty else 2019
max_year = int(df['ano_admissao'].max()) if not df['ano_admissao'].empty else 2024
year_range = st.sidebar.slider(
    "Período de Admissão",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Filtro de Setor Simplificado
setores = sorted(df['setor_simplificado'].unique().tolist())
setores_selecionados = st.sidebar.multiselect(
    "Setor de Atuação",
    options=setores,
    default=setores
)

# Aplicação dos filtros
df_filtered = df[
    (df['ano_admissao'] >= year_range[0]) &
    (df['ano_admissao'] <= year_range[1]) &
    (df['setor_simplificado'].isin(setores_selecionados))
]

st.sidebar.metric("Total de Registros", len(df_filtered))

if df_filtered.empty:
    st.warning("Nenhum dado corresponde aos filtros selecionados.")
    st.stop()

# --- KPIs (Key Performance Indicators) - Destaque Visual ---
st.header("Indicadores Chave de Desempenho")
col1, col2, col3, col4 = st.columns(4)

# Função para formatar o KPI
def format_currency(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# KPI 1: Remuneração Média Nominal
avg_remun = df_filtered['remun_media_nominal'].mean()
col1.metric(
    "Remuneração Média",
    format_currency(avg_remun),
    delta="vs. Período Anterior" # Placeholder para dar um toque visual
)

# KPI 2: Tempo Médio de Emprego
avg_tempo = df_filtered['tempo_emprego_meses'].mean()
col2.metric(
    "Tempo Médio de Emprego",
    f"{avg_tempo:.1f} meses",
    delta="Estabilidade" # Placeholder
)

# KPI 3: Taxa de Mobilidade Inter-UF
mobilidade_uf_count = df_filtered['mobilidade_uf'].value_counts(normalize=True).get('Sim', 0)
col3.metric(
    "Mobilidade Inter-UF",
    f"{mobilidade_uf_count:.1%}",
    delta="Expansão Geográfica" # Placeholder
)

# KPI 4: Carga Horária Média
avg_carga = df_filtered['carga_horaria'].mean()
col4.metric(
    "Carga Horária Média",
    f"{avg_carga:.1f} horas/semana",
    delta="Jornada Padrão" # Placeholder
)

st.markdown("---")

# --- Seção 1: Ocupação e Remuneração ---
st.header("Ocupação e Condições de Trabalho")
col_s1_1, col_s1_2 = st.columns(2)

# Gráfico 1.1: Top 10 Ocupações (CBO) - Gráfico de Barras Horizontal com cores vibrantes
cbo_counts = df_filtered['cbo_descricao'].value_counts().nlargest(10).reset_index()
cbo_counts.columns = ['Ocupação', 'Contagem']
fig_cbo = px.bar(
    cbo_counts,
    x='Contagem',
    y='Ocupação',
    orientation='h',
    title='Top 10 Ocupações Mais Frequentes',
    color='Contagem',
    color_continuous_scale=COLOR_SEQUENCE,
    labels={'Contagem': 'Número de Registros'}
)
fig_cbo.update_layout(yaxis={'categoryorder':'total ascending'})
col_s1_1.plotly_chart(fig_cbo, use_container_width=True)

# Gráfico 1.2: Remuneração Média por Setor Simplificado - Gráfico de Barras Vertical
remun_setor = df_filtered.groupby('setor_simplificado')['remun_media_nominal'].mean().reset_index()
remun_setor.columns = ['Setor', 'Remuneração Média']
fig_remun_setor = px.bar(
    remun_setor,
    x='Setor',
    y='Remuneração Média',
    title='Remuneração Média por Setor de Atuação',
    color='Setor',
    color_discrete_sequence=COLOR_SEQUENCE,
    labels={'Remuneração Média': 'Remuneração Média (R$)'}
)
col_s1_2.plotly_chart(fig_remun_setor, use_container_width=True)

st.markdown("---")

# --- Seção 2: Distribuição e Tendências ---
st.header("Distribuição e Tendências")
col_s2_1, col_s2_2 = st.columns(2)

# Gráfico 2.1: Distribuição por Natureza Jurídica (Top 5) - Gráfico de Pizza
nj_counts = df_filtered['natureza_juridica'].value_counts().nlargest(5).reset_index()
nj_counts.columns = ['Natureza Jurídica', 'Contagem']
fig_nj_pie = px.pie(
    nj_counts,
    values='Contagem',
    names='Natureza Jurídica',
    title='Top 5 Naturezas Jurídicas',
    hole=.4,
    color_discrete_sequence=COLOR_SEQUENCE
)
col_s2_1.plotly_chart(fig_nj_pie, use_container_width=True)

# Gráfico 2.2: Remuneração vs. Tempo de Emprego - Gráfico de Dispersão
fig_scatter = px.scatter(
    df_filtered,
    x='tempo_emprego_meses',
    y='remun_media_nominal',
    color='setor_simplificado',
    hover_data=['cbo_descricao', 'mun_trabalho'],
    title='Remuneração vs. Tempo de Emprego',
    color_discrete_sequence=COLOR_SEQUENCE,
    labels={'tempo_emprego_meses': 'Tempo de Emprego (meses)', 'remun_media_nominal': 'Remuneração Média (R$)'}
)
col_s2_2.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# --- Seção 3: Tabela Detalhada (Aba) ---
st.subheader("Dados Detalhados")
tab1, tab2 = st.tabs(["Tabela de Dados (Amostra)", "Distribuição de Carga Horária"])

with tab1:
    st.dataframe(df_filtered.head(100))

with tab2:
    fig_hist = px.histogram(
        df_filtered,
        x="carga_horaria",
        title="Distribuição da Carga Horária Contratada",
        color_discrete_sequence=[PRIMARY_COLOR],
        labels={'carga_horaria': 'Carga Horária (horas/semana)'}
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# --- Informações Adicionais ---
st.sidebar.markdown("---")
st.sidebar.markdown("Versão Visual e Intuitiva.")

import pandas as pd
import numpy as np

# Caminho para o arquivo de dados
FILE_PATH = "/home/ubuntu/upload/emprego_formal_administraco_2019_2024.xlsx"
OUTPUT_PATH = "cleaned_data.csv"

# Mapeamento de colunas para nomes mais amigáveis
COLUMN_MAPPING = {
    'Unnamed: 0': 'id_registro',
    'aluno': 'id_aluno',
    'municipio__nome': 'mun_formacao',
    'mun_trab__nome': 'mun_trabalho',
    'municipio__sigla_uf': 'uf_formacao',
    'mun_trab__sigla_uf': 'uf_trabalho',
    'cbo_ocupacao_2002__codigo': 'cbo_codigo',
    'cbo_ocupacao_2002__descricao': 'cbo_descricao',
    'cnae_20_subclasse': 'cnae_codigo',
    'cnae_20_subclasse__descricao_subclasse': 'cnae_descricao',
    'tipo_vinculo__descricao': 'tipo_vinculo',
    'natureza_juridica__descricao': 'natureza_juridica',
    'data_admissao_declarada': 'data_admissao',
    'vl_remun_media_nom': 'remun_media_nominal',
    'tempo_emprego': 'tempo_emprego_meses',
    'qtd_hora_contr': 'carga_horaria',
    'tipo_salario': 'tipo_salario_cod'
}

# Mapeamento simplificado para tipo de salário (baseado em códigos comuns do CAGED/RAIS)
SALARIO_MAP = {
    1: 'Mensal',
    2: 'Quinzenal',
    3: 'Semanal',
    4: 'Hora',
    5: 'Tarefa',
    6: 'Diário',
    99: 'Outros/Não Informado'
}

def load_and_clean_data(file_path):
    """Carrega, limpa e processa os dados."""
    print("Carregando dados...")
    df = pd.read_excel(file_path)

    # 1. Padronização das colunas
    df = df.rename(columns=COLUMN_MAPPING)
    df = df.drop(columns=['id_registro'], errors='ignore') # 'Unnamed: 0' é apenas um índice

    # 2. Tratamento de dados faltantes e inconsistências
    # Removendo registros com remuneração nominal zero ou nula
    df = df[df['remun_media_nominal'].notna() & (df['remun_media_nominal'] > 0)].copy()

    # Convertendo colunas para tipos apropriados
    df['data_admissao'] = pd.to_datetime(df['data_admissao'], errors='coerce')
    df['remun_media_nominal'] = pd.to_numeric(df['remun_media_nominal'], errors='coerce')
    df['tempo_emprego_meses'] = pd.to_numeric(df['tempo_emprego_meses'], errors='coerce')
    df['carga_horaria'] = pd.to_numeric(df['carga_horaria'], errors='coerce')
    df['tipo_salario_cod'] = df['tipo_salario_cod'].fillna(99).astype(int)

    # Limpeza de strings para filtros
    string_cols = ['mun_formacao', 'mun_trabalho', 'uf_formacao', 'uf_trabalho',
                   'cbo_descricao', 'tipo_vinculo', 'natureza_juridica']
    for col in string_cols:
        df[col] = df[col].astype(str).str.strip().str.title()

    # 3. Criação de variáveis derivadas

    # Indicador de mobilidade geográfica (entre municípios)
    df['mobilidade_mun'] = np.where(df['mun_formacao'] != df['mun_trabalho'], 'Sim', 'Não')

    # Indicador de mobilidade geográfica (entre UF)
    df['mobilidade_uf'] = np.where(df['uf_formacao'] != df['uf_trabalho'], 'Sim', 'Não')

    # Mapeamento do tipo de salário
    df['tipo_salario'] = df['tipo_salario_cod'].map(SALARIO_MAP).fillna('Outros/Não Informado')

    # Simplificação da Natureza Jurídica (Público, Privado, Terceiro Setor)
    def simplify_natureza_juridica(nj):
        nj = str(nj).lower()
        if 'órgão público' in nj or 'autarquia' in nj or 'fundação pública' in nj or 'servidor' in nj or 'empresa pública' in nj:
            return 'Setor Público'
        elif 'associação' in nj or 'serviço social autônomo' in nj:
            return 'Terceiro Setor'
        elif 'sociedade' in nj or 'empresário' in nj or 'empresa individual' in nj:
            return 'Setor Privado'
        else:
            return 'Outros'

    df['setor_simplificado'] = df['natureza_juridica'].apply(simplify_natureza_juridica)

    # Adicionando o ano e mês de admissão para análise temporal
    df['ano_admissao'] = df['data_admissao'].dt.year
    df['mes_ano_admissao'] = df['data_admissao'].dt.to_period('M').astype(str)

    # Filtrando colunas para o output
    columns_to_keep = [
        'id_aluno', 'mun_formacao', 'uf_formacao', 'mun_trabalho', 'uf_trabalho',
        'cbo_descricao', 'cnae_descricao', 'tipo_vinculo', 'natureza_juridica',
        'remun_media_nominal', 'tempo_emprego_meses', 'carga_horaria',
        'tipo_salario', 'mobilidade_mun', 'mobilidade_uf', 'setor_simplificado',
        'ano_admissao', 'mes_ano_admissao'
    ]
    df_cleaned = df[columns_to_keep]

    print(f"Dados limpos e processados. Total de registros: {len(df_cleaned)}")
    return df_cleaned

if __name__ == "__main__":
    try:
        df_cleaned = load_and_clean_data(FILE_PATH)
        df_cleaned.to_csv(OUTPUT_PATH, index=False)
        print(f"Dados salvos em {OUTPUT_PATH}")
    except Exception as e:
        print(f"Ocorreu um erro durante o processamento dos dados: {e}")
