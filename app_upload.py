import streamlit as st
import csv
import io

# Configuración de página
st.set_page_config(
    page_title="Consulta de Nómina",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Consulta de Nómina")
st.markdown("### Carga tu archivo y consulta tu información")

st.divider()

# Subida de archivo
archivo = st.file_uploader(
    "📎 Sube tu archivo CSV",
    type="csv",
    help="El archivo debe contener las columnas: Num. Per, Nombre, Fecha, Núm hojas"
)

def cargar_datos(archivo_csv):
    datos = {}

    archivo_texto = io.TextIOWrapper(archivo_csv, encoding="utf-8-sig")
    lector = csv.DictReader(archivo_texto)

    lector.fieldnames = [campo.strip() for campo in lector.fieldnames]

    columnas_requeridas = {"Num. Per", "Nombre", "Fecha", "Núm hojas"}

    if not columnas_requeridas.issubset(set(lector.fieldnames)):
        return None

    for fila in lector:
        fila = {k.strip(): v.strip() for k, v in fila.items()}

        num_per = fila["Num. Per"]
        nombre = fila["Nombre"]
        fecha = fila["Fecha"]
        num_hojas = fila["Núm hojas"]

        if num_per not in datos:
            datos[num_per] = {
                "nombre": nombre,
                "registros": []
            }

        datos[num_per]["registros"].append({
            "fecha": fecha,
            "num_hojas": num_hojas
        })

    return datos


if archivo is not None:

    datos = cargar_datos(archivo)

    if datos is None:
        st.error("❌ El archivo no contiene las columnas requeridas.")
        st.stop()

    st.success("✅ Archivo cargado correctamente.")

    st.divider()

    numero = st.text_input("🔎 Ingresa tu Número de Personal")

    if numero:
        if numero in datos:
            st.subheader("Resultado")

            st.markdown(f"**Nombre:** {datos[numero]['nombre']}")

            st.markdown("**Registros encontrados:**")

            for registro in datos[numero]["registros"]:
                st.write(
                    f"📅 {registro['fecha']}  |  📄 Núm hojas: {registro['num_hojas']}"
                )

        else:
            st.error("❌ Ese número de personal no existe en el archivo.")

else:
    st.info("👆 Primero debes subir un archivo CSV para comenzar.")