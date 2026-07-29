"""
Interface web da Imobiliária R.M feita com Streamlit.

Como executar (a partir da raiz do projeto):
    pip install -r requirements.txt
    streamlit run app_streamlit.py
"""

import streamlit as st
import tempfile, os
from scripts.models import Apartamento, Casa, Estudio
from scripts.orcamento import Contrato, OrcamentoAluguel

st.set_page_config(page_title="R.M Imobiliária - Orçamento de Aluguel",
                    page_icon="🏠", layout="centered")

st.markdown(
    """
    <style>
        .stApp { background-color: #12181f; color: #eaf0f5; }
        h1, h2, h3 { color: #eaf0f5 !important; }
        [data-testid="stMetricValue"] { color: #c9a15a; }
        [data-testid="stSidebar"] { background-color: #1a232d; }
        .stButton>button { background-color: #c9a15a; color: #1a1305; border: none; }
        .stDownloadButton>button { background-color: transparent; color: #c9a15a;
                                    border: 1px solid #c9a15a; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🏠 Imobiliária R.M")
st.caption("Orçamento de aluguel - monte a proposta de locação do cliente.")

# ==================================================================
# SIDEBAR
# ==================================================================
with st.sidebar:
    st.header("Dados do orçamento")

    nome_cliente = st.text_input("Nome do cliente", placeholder="Opcional")
    tipo = st.selectbox("Tipo de imóvel", ["Apartamento", "Casa", "Estúdio"])

    st.subheader("Configuração do imóvel")

    imovel = None

    if tipo == "Apartamento":
        quartos = st.selectbox("Quartos", [1, 2])
        garagem = st.checkbox("Vaga de garagem (+R$ 300,00)")
        sem_filhos = st.checkbox("Cliente sem filhos (desconto 5%)")
        imovel = Apartamento(quartos=quartos, garagem=garagem, sem_criancas=sem_filhos)

    elif tipo == "Casa":
        quartos = st.selectbox("Quartos", [1, 2])
        garagem = st.checkbox("Vaga de garagem (+R$ 300,00)")
        imovel = Casa(quartos=quartos, garagem=garagem)

    else:  # Estúdio
        quer_vagas = st.checkbox("Incluir vagas de estacionamento")
        vagas = 0
        if quer_vagas:
            vagas = st.slider("Quantidade de vagas", min_value=2, max_value=10, value=2)
        imovel = Estudio(vagas=vagas)

    st.subheader("Contrato de locação")
    st.caption("Valor fixo: R$ 2.000,00, parcelável em até 5x.")
    num_parcelas = st.slider("Número de parcelas", min_value=1, max_value=5, value=5)

contrato = Contrato(num_parcelas=num_parcelas)

# ==================================================================
# PÁGINA PRINCIPAL
# ==================================================================

orcamento = OrcamentoAluguel(imovel=imovel, contrato=contrato,
                              cliente=nome_cliente or "Cliente")

st.subheader("Resumo do orçamento")

m1, m2, m3 = st.columns(3)
m1.metric("Aluguel mensal", f"R$ {orcamento.valor_aluguel_mensal():.2f}")
m2.metric("Valor do contrato", "R$ 2.000,00")
m3.metric(f"Parcela ({num_parcelas}x)", f"R$ {contrato.valor_parcela():.2f}")

with st.expander("RESUMO", expanded=True):
    st.code(orcamento.resumo(), language=None)

caminho_csv = orcamento.exportar_csv(os.path.join(tempfile.gettempdir(), "orcamento_aluguel.csv"))
with open(caminho_csv, "rb") as f:
    st.download_button(
        label="⬇️ Baixar Orçamento (12 meses)",
        data=f,
        file_name="orcamento_aluguel.csv",
        mime="text/csv",
    )
