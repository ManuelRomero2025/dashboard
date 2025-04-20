import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Penguins 🐧", layout="wide")

@st.cache_data
def cargar_datos():
    return pd.read_csv("penguins_v1.csv")

df = cargar_datos()

st.title("📊 Dashboard Penguins - Filtros por Variable")

st.sidebar.header("🔍 Filtros personalizados")

species = st.sidebar.multiselect("Especie", df["species"].unique(), default=df["species"].unique())
island = st.sidebar.multiselect("Isla", df["island"].unique(), default=df["island"].unique())
sex = st.sidebar.multiselect("Sexo", df["sex"].dropna().unique(), default=df["sex"].dropna().unique())
year = st.sidebar.multiselect("Año", df["year"].unique(), default=df["year"].unique())

bill_length = st.sidebar.slider("Longitud del pico (mm)", float(df["bill_length_mm"].min()), float(df["bill_length_mm"].max()), (float(df["bill_length_mm"].min()), float(df["bill_length_mm"].max())))
bill_depth = st.sidebar.slider("Profundidad del pico (mm)", float(df["bill_depth_mm"].min()), float(df["bill_depth_mm"].max()), (float(df["bill_depth_mm"].min()), float(df["bill_depth_mm"].max())))
flipper_length = st.sidebar.slider("Longitud de aleta (mm)", int(df["flipper_length_mm"].min()), int(df["flipper_length_mm"].max()), (int(df["flipper_length_mm"].min()), int(df["flipper_length_mm"].max())))
body_mass = st.sidebar.slider("Masa corporal (g)", int(df["body_mass_g"].min()), int(df["body_mass_g"].max()), (int(df["body_mass_g"].min()), int(df["body_mass_g"].max())))

df_filtrado = df[
    (df["species"].isin(species)) &
    (df["island"].isin(island)) &
    (df["sex"].isin(sex)) &
    (df["year"].isin(year)) &
    (df["bill_length_mm"].between(*bill_length)) &
    (df["bill_depth_mm"].between(*bill_depth)) &
    (df["flipper_length_mm"].between(*flipper_length)) &
    (df["body_mass_g"].between(*body_mass))
]

st.subheader("📌 Resumen")
col1, col2 = st.columns(2)
col1.metric("Cantidad de registros", len(df_filtrado))
col2.metric("Masa corporal promedio", f"{df_filtrado['body_mass_g'].mean():,.2f} g")

st.subheader("📊 Dispersión: Longitud vs Profundidad del Pico")
fig, ax = plt.subplots()
sns.scatterplot(data=df_filtrado, x="bill_length_mm", y="bill_depth_mm", hue="species", ax=ax)
st.pyplot(fig)

st.subheader("📄 Datos filtrados")
st.dataframe(df_filtrado, use_container_width=True)
