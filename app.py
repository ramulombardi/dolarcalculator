import streamlit as st
import requests

# Función para obtener las cotizaciones desde DolarApi.com
@st.cache_data
def obtener_cotizaciones():
    url = "https://dolarapi.com/v1/dolares"
    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.RequestException as e:
        st.error(f"Error al obtener las cotizaciones: {e}")
        return []

# Función para realizar la conversión
def convertir(modo, monto, cotizacion):
    if modo == "Vender dólares":
        return monto * cotizacion["compra"]
    else:  # Comprar dólares
        return monto / cotizacion["venta"] if cotizacion["venta"] != 0 else 0

# Título de la aplicación
st.title("Dolar Calculator 🇺🇸💱🇦🇷")

# Obtener cotizaciones
cotizaciones = obtener_cotizaciones()



# Estilo de botones grandes
st.markdown("""
<style>
div.stButton > button {
    width: 100%;
    padding: 1rem;
    font-size: 1.2rem;
    font-weight: bold;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Botones grandes para elegir operación
st.subheader("Seleccioná la operación:")

col1, col2 = st.columns(2)
modo = None

with col1:
    if st.button("💰 Vender dólares"):
        modo = "Vender dólares"
with col2:
    if st.button("💵 Comprar dólares"):
        modo = "Comprar dólares"

# Guardar el modo en session_state si se hace clic
if modo:
    st.session_state["modo"] = modo

# Mostrar formulario solo si se eligió una opción
if "modo" in st.session_state:
    st.markdown(f"### Modo seleccionado: **{st.session_state['modo']}**")
    monto = st.number_input("Ingresa el monto:", min_value=0.0, format="%.2f")

    # Diccionario de cotizaciones
    opciones = {c["nombre"]: c for c in cotizaciones}
    nombres_cotizaciones = list(opciones.keys())

    seleccion = st.selectbox("Selecciona la cotización:", nombres_cotizaciones)
    cotizacion = opciones.get(seleccion)

    if cotizacion:
        resultado = convertir(st.session_state["modo"], monto, cotizacion)
        if st.session_state["modo"] == "Vender dólares":
            st.success(f"Recibirás ${resultado:,.2f} ARS.")
        else:
            st.success(f"Podrás comprar USD {resultado:,.2f}.")
    else:
        st.warning("No se encontró la cotización seleccionada.")


# Mostrar cotizaciones en tarjetas
if cotizaciones:
    st.subheader("💵 Cotizaciones actuales")
    for i in range(0, len(cotizaciones), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(cotizaciones):
                c = cotizaciones[i + j]
                with col:
                    st.markdown(
                        f"""
                        <div style="
                            background-color: #1c1c1e;
                            padding: 1rem;
                            border-radius: 12px;
                            margin-bottom: 1rem;
                            color: white;
                            text-align: center;
                            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                        ">
                            <h4 style="margin-bottom: 0.5rem;">{c['nombre']}</h4>
                            <p><strong>Compra:</strong> ${c['compra']:,.2f}</p>
                            <p><strong>Venta:</strong> ${c['venta']:,.2f}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
else:
    st.warning("No se pudieron obtener las cotizaciones.")
    st.stop()

# Separador visual
st.markdown("---")