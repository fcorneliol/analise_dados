import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuração da página: título da aba, favicon e layout wide
st.set_page_config(
    page_title="Dashboard - Meio de Transporte",
    page_icon="🚌",
    layout="wide"
)

st.title("Dashboard - Meio de Transporte ao Trabalho (Mulheres)")
st.write("__________________________________________________________")

PATH = "Tabela_13_Meio_de_transporte.xlsx"

# ---------------------------------------------------------------
# Carregamento dos dados (com cache para não reler toda hora)
# ---------------------------------------------------------------
@st.cache_data
def carregar_brasil():
    df = pd.read_excel(PATH, skiprows=1, sheet_name=1)
    df = df.dropna(subset=["Meio de transporte/cor ou raça"])
    return df


@st.cache_data
def carregar_locais():
    df = pd.read_excel(PATH, sheet_name="BR GR UF MU", skiprows=2, header=None)
    colunas = ['Local',
               'Branca_A pé', 'Branca_Bicicleta', 'Branca_Motocicleta', 'Branca_Carro', 'Branca_Coletivo', 'Branca_Outros',
               'PretaParda_A pé', 'PretaParda_Bicicleta', 'PretaParda_Motocicleta', 'PretaParda_Carro', 'PretaParda_Coletivo', 'PretaParda_Outros',
               'Indigena_A pé', 'Indigena_Bicicleta', 'Indigena_Motocicleta', 'Indigena_Carro', 'Indigena_Coletivo', 'Indigena_Outros']
    df = df.iloc[:, :19]
    df.columns = colunas
    df['Local'] = df['Local'].astype(str).str.strip()

    df_longo = df.melt(id_vars=['Local'], value_vars=colunas[1:],
                       var_name="Categoria", value_name="Percentual")
    df_longo['Percentual'] = pd.to_numeric(
        df_longo['Percentual'].replace(['-', ' ', '.', 'nan'], np.nan),
        errors='coerce'
    ).fillna(0)
    df_longo[['Raca', 'Transporte']] = df_longo['Categoria'].str.split('_', expand=True)

    df_geral = df_longo.groupby(['Local', 'Transporte'])['Percentual'].mean().reset_index()
    return df_geral


estados = ['Rondônia', 'Acre', 'Amazonas', 'Roraima', 'Pará', 'Amapá', 'Tocantins', 'Maranhão', 'Piauí', 'Ceará',
           'Rio Grande do Norte', 'Paraíba', 'Pernambuco', 'Alagoas', 'Sergipe', 'Bahia', 'Minas Gerais',
           'Espírito Santo', 'Rio de Janeiro', 'São Paulo', 'Paraná', 'Santa Catarina', 'Rio Grande do Sul',
           'Mato Grosso do Sul', 'Mato Grosso', 'Goiás', 'Distrito Federal']
excluir = estados + ['Brasil', 'Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-oeste', 'nan']

df = carregar_brasil()
df_geral = carregar_locais()
df_est = df_geral[df_geral['Local'].isin(estados)]
df_cid = df_geral[~df_geral['Local'].isin(excluir)]

grupos = ['Branca', 'Preta ou parda', 'Indígena']
cores = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6']

# ---------------------------------------------------------------
# PARTE 1 - Brasil por cor/raça
# ---------------------------------------------------------------
st.header("Parte 1 - Brasil por cor/raça")
st.subheader("Como as mulheres vão ao trabalho em cada grupo")
st.write("__________________________________________________________")

st.write("### Tabela de dados (%):")
st.dataframe(df, use_container_width=True, hide_index=True)

grupos_selecionados = st.multiselect(
    "Escolha os grupos para ver nos gráficos de pizza:",
    grupos,
    default=grupos
)

if grupos_selecionados:
    colunas_graficos = st.columns(len(grupos_selecionados))
    for i, grupo in enumerate(grupos_selecionados):
        with colunas_graficos[i]:
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(
                df[grupo],
                labels=df['Meio de transporte/cor ou raça'],
                autopct='%1.3f%%',
                startangle=180,
                colors=cores,
                wedgeprops={'edgecolor': 'white', 'linewidth': 1.2},
            )
            ax.set_title(f'Cor/Raça: {grupo}', fontsize=12, fontweight='bold')
            st.pyplot(fig)
            plt.close(fig)
else:
    st.write("Selecione pelo menos um grupo para ver os gráficos.")

st.write("__________________________________________________________")

st.write("### Análise de diferenças")
col_info, col_resultado = st.columns([2, 1])

with col_info:
    with st.form('comparar_grupos'):
        transporte = st.selectbox("Meio de transporte:", df['Meio de transporte/cor ou raça'])
        botao_comparar = st.form_submit_button('Comparar grupos')

if botao_comparar:
    linha = df[df['Meio de transporte/cor ou raça'] == transporte].iloc[0]
    with col_resultado:
        st.write(f"### {transporte}")
        st.metric("Brancas x Pretas/Pardas", f"{abs(linha['Branca'] - linha['Preta ou parda']):.1f}%")
        st.metric("Brancas x Indígenas", f"{abs(linha['Branca'] - linha['Indígena']):.1f}%")
        st.metric("Pretas/Pardas x Indígenas", f"{abs(linha['Preta ou parda'] - linha['Indígena']):.1f}%")

st.write("__________________________________________________________")

# ---------------------------------------------------------------
# PARTE 2 - Estados e cidades
# ---------------------------------------------------------------
st.header("Parte 2 - Estados e cidades")
st.subheader("Média entre os grupos de cor/raça")
st.write("__________________________________________________________")

c1, c2, c3, c4 = st.columns(4)
coletivo = df_est[df_est['Transporte'] == 'Coletivo']
bike = df_cid[df_cid['Transporte'] == 'Bicicleta']
carro = df_cid[df_cid['Transporte'] == 'Carro']
c1.metric("Mais coletivo (estado)", coletivo.loc[coletivo['Percentual'].idxmax(), 'Local'])
c2.metric("Menos coletivo (estado)", coletivo.loc[coletivo['Percentual'].idxmin(), 'Local'])
c3.metric("Mais bicicleta (cidade)", bike.loc[bike['Percentual'].idxmax(), 'Local'])
c4.metric("Mais carro (cidade)", carro.loc[carro['Percentual'].idxmax(), 'Local'])

st.write("__________________________________________________________")

transporte_escolhido = st.selectbox(
    "Escolha um meio de transporte para o ranking:",
    sorted(df_geral['Transporte'].unique())
)

col_est, col_cid = st.columns(2)

with col_est:
    st.write(f"### Estados - {transporte_escolhido}")
    ranking_est = (df_est[df_est['Transporte'] == transporte_escolhido]
                   .sort_values('Percentual', ascending=False)
                   .set_index('Local')['Percentual'])
    st.bar_chart(ranking_est)

with col_cid:
    qtd = st.slider("Quantas cidades mostrar no top?", 5, 30, 10)
    st.write(f"### Top {qtd} cidades - {transporte_escolhido}")
    ranking_cid = (df_cid[df_cid['Transporte'] == transporte_escolhido]
                   .sort_values('Percentual', ascending=False)
                   .head(qtd)[['Local', 'Percentual']])
    st.dataframe(ranking_cid, use_container_width=True, hide_index=True)

st.write("__________________________________________________________")

st.write("### Perfil de um local")
local = st.selectbox("Pesquise um estado ou cidade:", sorted(df_geral['Local'].unique()))
perfil = df_geral[df_geral['Local'] == local].set_index('Transporte')['Percentual']
st.bar_chart(perfil)
