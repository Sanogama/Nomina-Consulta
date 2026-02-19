import streamlit as st
import csv

st.title("📄 Consulta de Nómina")

def cargar_datos():
    datos = {}

    try:
        with open("Nomina.csv", newline="", encoding="utf-8-sig") as archivo:
            lector = csv.DictReader(archivo)
            lector.fieldnames = [campo.strip() for campo in lector.fieldnames]

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

    except FileNotFoundError:
        st.error("No se encontró el archivo Nomina.csv")
        return {}

    return datos


datos = cargar_datos()

if datos:
    num_buscar = st.text_input("Ingresa el Número de Personal")

    if num_buscar:
        if num_buscar in datos:
            st.success("Resultado encontrado")

            st.write("Nombre:", datos[num_buscar]["nombre"])
            st.write("Fechas en las que aparece:")

            for registro in datos[num_buscar]["registros"]:
                texto = f"- {registro['fecha']}"
                if registro["num_hojas"]:
                    texto += f" | Núm hojas: {registro['num_hojas']}"
                st.write(texto)
        else:
            st.error("Ese número de personal no existe.")
