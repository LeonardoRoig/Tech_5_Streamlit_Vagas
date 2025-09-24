
import json, pandas as pd, streamlit as st
from train_and_rank import run_pipeline

st.set_page_config(page_title="Netflix das Vagas", layout="wide")
st.title("🎬 Netflix das Vagas — Top 10 Candidatos por Vaga")

train_file = st.file_uploader("CSV de treino (aprovados/reprovados)", type=["csv"])
pending_file = st.file_uploader("CSV de pendentes (não classificados)", type=["csv"])

if train_file and pending_file:
    with open("train.csv","wb") as f: f.write(train_file.getbuffer())
    with open("pending.csv","wb") as f: f.write(pending_file.getbuffer())
    ranking = run_pipeline("train.csv", "pending.csv", export_dir=".")
    st.success("Pipeline executado!")

    vagas = sorted(ranking["id_vaga"].unique().tolist())
    vaga_sel = st.sidebar.selectbox("Selecione a vaga", vagas)
    top = ranking[ranking["id_vaga"]==vaga_sel].sort_values("rank")
    st.subheader(f"Top {len(top)} candidatos para a vaga {vaga_sel}")

    cols = st.columns(5)
    for i, (_, row) in enumerate(top.iterrows()):
        col = cols[i % 5]
        with col:
            st.markdown(f"### 👤 Candidato {row['id_candidato']}")
            st.metric("Score (modelo)", f"{row['score']:.3f}")
            st.caption(f"Rank: {row['rank']}")
    with st.expander("Tabela completa da vaga"):
        st.dataframe(top)
else:
    st.info("Faça upload dos dois arquivos CSV para rodar o pipeline.")
