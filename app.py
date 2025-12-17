import streamlit as st
import pandas as pd

st.set_page_config(page_title="Categorizador de Médicos", layout="wide")

st.title("🩺 Clasificador Estratégico de Médicos")
st.markdown("Sube tu archivo CSV de Algología para segmentar a los médicos automáticamente.")

archivo = st.file_uploader("Selecciona el archivo CSV", type=["csv"])

if archivo:
    df = pd.read_csv(archivo)
    
    # Limpieza y Cálculo
    presc_cols = ['oxicodona', 'metadona', 'hidromorfona', 'morfina', 'buprenorfina', 'nalbufina', 'fentanilo']
    df[presc_cols] = df[presc_cols].fillna(0)
    df['total_recetas'] = df[presc_cols].sum(axis=1)
    
    def asignar_categoria(row):
        # Puntos por pacientes
        p_score = 3 if row['numero_pacientes'] > 55 else (2 if row['numero_pacientes'] >= 20 else 1)
        # Puntos por recetas
        r_score = 3 if row['total_recetas'] > 32 else (2 if row['total_recetas'] >= 13 else 1)
        
        total = p_score + r_score
        if total >= 5: return 'Estratégico (Alto Impacto)'
        if total >= 3: return 'En Desarrollo (Medio Impacto)'
        return 'Potencial Base (Bajo Impacto)'

    df['Categoria'] = df.apply(asignar_categoria, axis=1)

    # Métricas rápidas
    col1, col2, col3 = st.columns(3)
    col1.metric("Médicos Estratégicos", len(df[df['Categoria'] == 'Estratégico (Alto Impacto)']))
    col2.metric("En Desarrollo", len(df[df['Categoria'] == 'En Desarrollo (Medio Impacto)']))
    col3.metric("Potencial Base", len(df[df['Categoria'] == 'Potencial Base (Bajo Impacto)']))

    # Buscador
    busqueda = st.text_input("🔍 Buscar médico por nombre:")
    if busqueda:
        df_mostrar = df[df['nombre_medico'].str.contains(busqueda, case=False, na=False)]
    else:
        df_mostrar = df

    # Mostrar Tabla
    st.dataframe(df_mostrar[['nombre_medico', 'especialidad_neol', 'numero_pacientes', 'total_recetas', 'Categoria']])

    # Descarga
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar Reporte Categorizado", csv, "medicos_categorizados.csv", "text/csv")