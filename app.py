import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Controle Fitness", page_icon="🏋️")

ARQUIVO = "dados.csv"

# ===== BASE DE ALIMENTOS (AMPLIADA) =====
alimentos = {
    # Proteínas
    "Frango grelhado (100g)": [165, 31, 0, 3],
    "Carne magra (100g)": [180, 26, 0, 8],
    "Peixe grelhado (100g)": [140, 26, 0, 3],
    "Ovo inteiro (1 un)": [70, 6, 1, 5],
    "Atum (lata)": [120, 26, 0, 1],
    "Whey (30g)": [120, 24, 3, 2],

    # Carboidratos
    "Arroz cozido (100g)": [130, 2, 28, 1],
    "Feijão (100g)": [90, 6, 14, 1],
    "Batata doce (100g)": [90, 2, 21, 0],
    "Macarrão cozido (100g)": [150, 5, 30, 2],
    "Aveia (40g)": [150, 5, 27, 3],
    "Granola (30g)": [130, 3, 20, 4],
    "Pão integral (1 fatia)": [70, 3, 12, 1],

    # Frutas
    "Banana (1 un)": [90, 1, 23, 0],
    "Maçã (1 un)": [80, 0, 21, 0],
    "Laranja (1 un)": [70, 1, 18, 0],
    "Mamão (100g)": [45, 0, 11, 0],
    "Manga (100g)": [60, 0, 15, 0],
    "Abacaxi (100g)": [50, 0, 13, 0],
    "Morango (100g)": [32, 1, 8, 0],
    "Uva (100g)": [70, 0, 18, 0],

    # Açaí
    "Açaí puro (100g)": [70, 1, 4, 5],
    "Açaí com xarope (100g)": [110, 1, 21, 4],
    "Açaí bowl (300g)": [330, 5, 63, 12],

    # Gorduras / extras
    "Azeite (10g)": [90, 0, 0, 10],
    "Pasta de amendoim (15g)": [90, 4, 3, 8],
    "Castanhas (10 un)": [70, 2, 3, 6],
    "Queijo coalho (50g)": [150, 8, 1, 12],
    "Chocolate 70% (20g)": [120, 2, 8, 9],
    "Cerveja (long neck)": [150, 1, 13, 0]
}

# ===== METs =====
exercicios = {
    "Musculação": 6.0,
    "Caminhada (esteira)": 4.3,
    "Corrida leve": 9.8,
    "Bicicleta": 7.5,
    "Elíptico": 8.0,
    "HIIT": 10.0
}

def kcal_gasta(met, peso, minutos):
    return round((met * 3.5 * peso / 200) * minutos, 1)

# ===== SESSION STATE =====
if "lista_exercicios" not in st.session_state:
    st.session_state.lista_exercicios = []

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

# ==============================
# ➕ NOVO DIA
# ==============================
st.header("➕ Novo dia")

data = st.date_input("Data", date.today())
peso = st.number_input("Peso do dia (kg)", 80.0, 200.0, step=0.1)

# ---------- ALIMENTAÇÃO ----------
st.subheader("🥗 Alimentação")
kcal = prot = carb = gord = 0

for alimento, v in alimentos.items():
    qtd = st.number_input(alimento, 0, 10, 0, key=f"food_{alimento}")
    kcal += v[0] * qtd
    prot += v[1] * qtd
    carb += v[2] * qtd
    gord += v[3] * qtd

# ---------- EXERCÍCIOS ----------
st.subheader("🏃 Exercícios do dia")

col1, col2, col3 = st.columns(3)

with col1:
    tipo_ex = st.selectbox("Exercício", exercicios.keys())
with col2:
    tempo = st.number_input("Tempo (min)", 0, 300, 0)
with col3:
    if st.button("➕ Adicionar exercício"):
        kcal_ex = kcal_gasta(exercicios[tipo_ex], peso, tempo)
        st.session_state.lista_exercicios.append(
            {"Exercício": tipo_ex, "Min": tempo, "kcal": kcal_ex}
        )

# Lista de exercícios adicionados
total_kcal_gasta = 0
if st.session_state.lista_exercicios:
    st.markdown("### 📋 Exercícios registrados")
    for i, ex in enumerate(st.session_state.lista_exercicios):
        st.write(f"- {ex['Exercício']} | {ex['Min']} min | {ex['kcal']} kcal")
        total_kcal_gasta += ex["kcal"]

saldo = kcal - total_kcal_gasta

st.divider()

# ---------- RESULTADOS ----------
st.subheader("📊 Resultado do dia")
st.metric("🔥 Calorias ingeridas", kcal)
st.metric("🔥 Calorias gastas", total_kcal_gasta)
st.metric("⚖️ Saldo calórico", saldo)
st.metric("🥩 Proteína", prot)
st.metric("🍚 Carbo", carb)
st.metric("🫒 Gordura", gord)

# ---------- SALVAR ----------
if st.button("💾 Salvar dia"):
    if data in df["Data"].dt.date.values:
        st.error("⚠️ Dia já existe. Use editar.")
    else:
        novo = pd.DataFrame([{
            "Data": data,
            "Peso": peso,
            "Calorias_Ingeridas": kcal,
            "Calorias_Gastas": total_kcal_gasta,
            "Saldo": saldo,
            "Proteina": prot,
            "Carbo": carb,
            "Gordura": gord
        }])
        df = pd.concat([df, novo], ignore_index=True)
        df.to_csv(ARQUIVO, index=False)
        st.session_state.lista_exercicios = []
        st.success("✅ Dia salvo com sucesso!")

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

