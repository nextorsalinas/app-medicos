import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Categorizador Biogentec", layout="wide")

st.title("Clasificador Médicos Algologia")
st.markdown("Sube tu archivo para segmentar a los médicos.")

# Cargador de archivos Excel
archivo = st.file_uploader("Selecciona el archivo Excel", type=["xlsx"])

if archivo:
    # Lectura de Excel
    df = pd.read_excel(archivo)
    
    # Definición de columnas de medicamentos
    presc_cols = ['oxicodona', 'metadona', 'hidromorfona', 'morfina', 'buprenorfina', 'nalbufina', 'fentanilo']
    
    # Limpieza: Asegurar que las columnas existen y rellenar vacíos con 0
    cols_presentes = [c for c in presc_cols if c in df.columns]
    df[cols_presentes] = df[cols_presentes].fillna(0)
    df['total_recetas'] = df[cols_presentes].sum(axis=1)
    
    # Lógica de Categorización
    def asignar_categoria(row):
        # Puntos por pacientes (Basado en el análisis de tus datos)
        p_score = 3 if row['numero_pacientes'] > 55 else (2 if row['numero_pacientes'] >= 20 else 1)
        # Puntos por recetas
        r_score = 3 if row['total_recetas'] > 32 else (2 if row['total_recetas'] >= 13 else 1)
        
        total = p_score + r_score
        if total >= 5: return 'Categoria 1 (Alto Impacto)'
        if total >= 3: return 'Categoria 2 (Medio Impacto)'
        return 'Categoria 3 (Bajo Impacto)'

    df['Categoria'] = df.apply(asignar_categoria, axis=1)

    # Panel de Métricas
    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("Médicos Estratégicos", len(df[df['Categoria'] == 'Categoria 1 (Alto Impacto)']))
    col2.metric("En Desarrollo", len(df[df['Categoria'] == 'Categoria 2 (Medio Impacto)']))
    col3.metric("Potencial Base", len(df[df['Categoria'] == 'Categoria 3 (Bajo Impacto)']))
    st.divider()

    # Buscador en tiempo real
    busqueda = st.text_input("🔍 Buscar médico por nombre:")
    if busqueda:
        df_mostrar = df[df['nombre_medico'].str.contains(busqueda, case=False, na=False)]
    else:
        df_mostrar = df

    # Vista previa de la tabla clasificada
    st.subheader("Vista Previa de Resultados")
    st.dataframe(df_mostrar[['nombre_medico', 'especialidad_neol', 'numero_pacientes', 'total_recetas', 'Categoria']], use_container_width=True)

    # Lógica para descargar en formato Excel (.xlsx)
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Categorizacion')
    
    st.download_button(
        label="📥 Descargar Reporte en Excel",
        data=buffer.getvalue(),
        file_name="medicos_categorizados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )







