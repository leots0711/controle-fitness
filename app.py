import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Controle Fitness", page_icon="🏋️")

# ===== BASE DE ALIMENTOS =====
alimentos = {
    "Frango grelhado (100g)": [165, 31, 0, 3],
    "Carne magra (100g)": [180, 26, 0, 8],
    "Ovo inteiro (1 un)": [70, 6, 1, 5],
    "Arroz cozido (100g)": [130, 2, 28, 1],
    "Feijão (100g)": [90, 6, 14, 1],
    "Batata doce (100g)": [90, 2, 21, 0],
    "Aveia (40g)": [150, 5, 27, 3],
    "Banana (1 un)": [90, 1, 23, 0],
    "Whey (30g)": [120, 24, 3, 2],
    "Azeite (10g)": [90, 0, 0, 10],
    "Cerveja (long neck)": [150, 1, 13, 0]
}

# ===== DADOS =====
ARQUIVO = "dados.csv"

try:
    df = pd.read_csv(ARQUIVO)
except:
    df = pd.DataFrame(columns=[
        "Data","Peso","Calorias","Proteina",
        "Carbo","Gordura","Treino","Cardio","Jejum","Alcool"
    ])

st.title("🏋️ Controle de Dieta & Treino")

st.markdown("""
**Metas diárias**
- 🔥 2350 kcal
- 🥩 220 g proteína
- 🍚 200 g carbo
- 🫒 70 g gordura
""")

# ===== REGISTRO =====
st.subheader("📅 Registro Diário")
data = st.date_input("Data", date.today())
peso = st.number_input("Peso (kg)", 80.0, 200.0, step=0.1)

st.subheader("🥗 Alimentação do dia")

total_kcal = total_prot = total_carb = total_gord = 0

for alimento, valores in alimentos.items():
    qtd = st.number_input(f"{alimento} - quantidade", 0, 10, 0)
    total_kcal += valores[0] * qtd
    total_prot += valores[1] * qtd
    total_carb += valores[2] * qtd
    total_gord += valores[3] * qtd

st.divider()

st.subheader("📊 Consumo do dia")
st.metric("🔥 Calorias", f"{total_kcal} kcal")
st.metric("🥩 Proteína", f"{total_prot} g")
st.metric("🍚 Carboidrato", f"{total_carb} g")
st.metric("🫒 Gordura", f"{total_gord} g")

st.divider()

treino = st.checkbox("🏋️ Treinou?")
cardio = st.slider("🚴 Cardio (min)", 0, 120, 0)
jejum = st.checkbox("⏱️ Fez jejum?")
alcool = st.checkbox("🍺 Consumiu álcool?")

if st.button("💾 Salvar dia"):
    novo = pd.DataFrame([{
        "Data": data,
        "Peso": peso,
        "Calorias": total_kcal,
        "Proteina": total_prot,
        "Carbo": total_carb,
        "Gordura": total_gord,
        "Treino": treino,
        "Cardio": cardio,
        "Jejum": jejum,
        "Alcool": alcool
    }])

    df = pd.concat([df, novo], ignore_index=True)
    df.to_csv(ARQUIVO, index=False)
    st.success("✅ Dia registrado!")

# ===== HISTÓRICO =====
if not df.empty:
    st.subheader("📈 Evolução do peso")
    df["Data"] = pd.to_datetime(df["Data"])
    st.line_chart(df.set_index("Data")["Peso"])

