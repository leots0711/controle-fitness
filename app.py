import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Controle Fitness Pessoal",
    page_icon="🏋️",
    layout="centered"
)

ARQUIVO = "dados.csv"

# ======= CARREGAR / CRIAR BASE =======
if ARQUIVO not in st.session_state:
    try:
        df = pd.read_csv(ARQUIVO)
    except:
        df = pd.DataFrame(columns=[
            "Data", "Peso", "Calorias", "Proteina",
            "Carbo", "Gordura", "Treino",
            "Tipo_Treino", "Cardio_min",
            "Jejum", "Alcool", "Observacoes"
        ])
    st.session_state.df = df

df = st.session_state.df

# ======= TÍTULO =======
st.title("🏋️ Controle Pessoal de Emagrecimento")

st.markdown("""
**Meta diária**
- 🔥 Calorias: **2350 kcal**
- 🥩 Proteína: **220 g**
- 🍚 Carbo: **200 g**
- 🫒 Gordura: **70 g**
""")

st.divider()

# ======= REGISTRO DIÁRIO =======
st.subheader("📅 Registro do Dia")

data = st.date_input("Data", date.today())

# Impede duplicar dia
if data in pd.to_datetime(df["Data"]).dt.date.values:
    st.warning("⚠️ Já existe registro para esta data. Edite no histórico.")
    st.stop()

peso = st.number_input("Peso (kg)", 80.0, 200.0, step=0.1)

col1, col2, col3 = st.columns(3)
with col1:
    calorias = st.number_input("Calorias", value=2350)
with col2:
    proteina = st.number_input("Proteína (g)", value=220)
with col3:
    carbo = st.number_input("Carbo (g)", value=200)

gordura = st.number_input("Gordura (g)", value=70)

treino = st.checkbox("🏋️ Treino realizado?")
tipo_treino = st.selectbox(
    "Tipo de treino",
    ["Nenhum", "Peito/Tríceps", "Costas/Bíceps", "Pernas", "Ombro/Core"]
)

cardio = st.slider("🚴 Cardio (min)", 0, 120, 0, step=5)
jejum = st.checkbox("⏱️ Fez jejum?")
alcool = st.checkbox("🍺 Consumiu álcool?")
obs = st.text_area("📝 Observações")

if st.button("💾 Salvar dia"):
    novo = pd.DataFrame([{
        "Data": data,
        "Peso": peso,
        "Calorias": calorias,
        "Proteina": proteina,
        "Carbo": carbo,
        "Gordura": gordura,
        "Treino": treino,
        "Tipo_Treino": tipo_treino,
        "Cardio_min": cardio,
        "Jejum": jejum,
        "Alcool": alcool,
        "Observacoes": obs
    }])

    df = pd.concat([df, novo], ignore_index=True)
    df.to_csv(ARQUIVO, index=False)
    st.session_state.df = df
    st.success("✅ Dia registrado com sucesso!")

st.divider()

# ======= ANÁLISE =======
if not df.empty:
    df["Data"] = pd.to_datetime(df["Data"])
    df = df.sort_values("Data")

    st.subheader("📈 Evolução do Peso")
    st.line_chart(df.set_index("Data")["Peso"])

    st.subheader("📊 Média Semanal")
    df["Semana"] = df["Data"].dt.to_period("W").astype(str)
    media = df.groupby("Semana")["Peso"].mean()
    st.bar_chart(media)

    st.subheader("📋 Últimos Registros")
    st.dataframe(df.tail(7), use_container_width=True)

    # Indicadores rápidos
    st.subheader("✅ Consistência (últimos 7 dias)")
    ultimos = df.tail(7)
    st.metric("Treinos realizados", int(ultimos["Treino"].sum()), "/ 7")
    st.metric("Dias com álcool", int(ultimos["Alcool"].sum()), "/ 7")
    st.metric("Média de cardio (min)", int(ultimos["Cardio_min"].mean()))
