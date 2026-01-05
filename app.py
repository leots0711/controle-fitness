import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Controle Fitness", page_icon="🏋️")

ARQUIVO = "dados.csv"

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

# ===== METs DOS EXERCÍCIOS =====
exercicios = {
    "Nenhum": 0,
    "Musculação": 6.0,
    "Caminhada (esteira)": 4.3,
    "Corrida leve": 9.8,
    "Bicicleta": 7.5,
    "Elíptico": 8.0,
    "HIIT": 10.0
}

# ===== FUNÇÃO DE CÁLCULO =====
def calorias_gastas(met, peso, minutos):
    return round((met * 3.5 * peso / 200) * minutos, 1)

# ===== CARREGAR DADOS =====
try:
    df = pd.read_csv(ARQUIVO)
except:
    df = pd.DataFrame(columns=[
        "Data","Peso","Calorias_Ingeridas","Calorias_Gastas",
        "Saldo","Proteina","Carbo","Gordura"
    ])

df["Data"] = pd.to_datetime(df["Data"], errors="coerce")

st.title("🏋️ Controle de Dieta, Exercício & Calorias")

st.markdown("""
**Metas**
- 🔥 2350 kcal ingeridas
- 🥩 220 g proteína
- 🍚 200 g carbo
- 🫒 70 g gordura
""")

# ==============================
# ➕ NOVO REGISTRO
# ==============================
st.header("➕ Novo dia")

data = st.date_input("Data", date.today())
peso = st.number_input("Peso do dia (kg)", 80.0, 200.0, step=0.1)

# ----- Alimentação -----
st.subheader("🥗 Alimentação")
kcal = prot = carb = gord = 0

for alimento, v in alimentos.items():
    qtd = st.number_input(alimento, 0, 10, 0, key=f"novo_{alimento}")
    kcal += v[0] * qtd
    prot += v[1] * qtd
    carb += v[2] * qtd
    gord += v[3] * qtd

# ----- Exercício -----
st.subheader("🏃 Exercício")
tipo_ex = st.selectbox("Tipo de exercício", exercicios.keys())
tempo = st.slider("Tempo (min)", 0, 180, 0)

kcal_gastas = calorias_gastas(exercicios[tipo_ex], peso, tempo)
saldo = kcal - kcal_gastas

st.divider()

# ----- Resultados -----
st.subheader("📊 Resultado do dia")
st.metric("🔥 Calorias ingeridas", kcal)
st.metric("🔥 Calorias gastas (ajustadas ao peso)", kcal_gastas)
st.metric("⚖️ Saldo calórico", saldo)
st.metric("🥩 Proteína", prot)
st.metric("🍚 Carbo", carb)
st.metric("🫒 Gordura", gord)

# ----- Salvar -----
if st.button("💾 Salvar dia"):
    if data in df["Data"].dt.date.values:
        st.error("⚠️ Dia já lançado. Use editar.")
    else:
        novo = pd.DataFrame([{
            "Data": data,
            "Peso": peso,
            "Calorias_Ingeridas": kcal,
            "Calorias_Gastas": kcal_gastas,
            "Saldo": saldo,
            "Proteina": prot,
            "Carbo": carb,
            "Gordura": gord
        }])
        df = pd.concat([df, novo], ignore_index=True)
        df.to_csv(ARQUIVO, index=False)
        st.success("✅ Registro salvo!")

st.divider()

# ==============================
# 📈 HISTÓRICO
# ==============================
if not df.empty:
    st.header("📈 Evolução do peso")
    df = df.sort_values("Data")
    st.line_chart(df.set_index("Data")["Peso"])

    st.header("📉 Saldo calórico")
    st.bar_chart(df.set_index("Data")["Saldo"])

