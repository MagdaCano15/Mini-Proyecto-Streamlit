import streamlit as st
import pandas as pd

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║                                                                         ║
# ║                 SECCION DE CALCULOS — NO MODIFICAR                      ║
# ║                                                                         ║
# ║  Aqui se encuentran las funciones que usted va a utilizar en los        ║
# ║  pasos de mas abajo. Lea los comentarios de cada una para entender      ║
# ║  que retorna y como usarla.                                             ║
# ║                                                                         ║
# ╚═══════════════════════════════════════════════════════════════════════════╝


def calcular_resumen(df: pd.DataFrame) -> dict:
    """
    Calcula un resumen general de los datos.

    Retorna un diccionario con:
        "ventas"   -> float, suma total de ventas
        "ganancia" -> float, suma total de ganancia
        "ordenes"  -> int, cantidad de ordenes unicas
    """
    return {
        "ventas": round(df["Ventas"].sum(), 2),
        "ganancia": round(df["Ganancia"].sum(), 2),
        "ordenes": df["ID_Orden"].nunique(),
    }


def ventas_por_mes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa las ventas por mes.

    Retorna un DataFrame con columnas: Año_Mes, Ventas
    Ordenado de manera cronologica.
    """
    df = df.copy()
    df["Año_Mes"] = pd.to_datetime(df["Fecha_Orden"]).dt.to_period("M").astype(str)
    return (
        df.groupby("Año_Mes")["Ventas"].sum()
        .reset_index().sort_values("Año_Mes")
        .round(2)
    )


def ventas_por_categoria(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa las ventas por categoria de producto.

    Retorna un DataFrame con columnas: Categoria, Ventas
    """
    return (
        df.groupby("Categoria")["Ventas"].sum()
        .reset_index().sort_values("Ventas", ascending=False)
        .round(2)
    )


def ventas_por_region(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa las ventas por region geografica.

    Retorna un DataFrame con columnas: Region, Ventas
    """
    return (
        df.groupby("Region")["Ventas"].sum()
        .reset_index().sort_values("Ventas", ascending=False)
        .round(2)
    )


def filtrar_datos(df, años=None, categorias=None, regiones=None):
    """
    Filtra el DataFrame segun los parametros indicados.
    Si un parametro es None, no aplica ese filtro.

    Parametros:
        df: DataFrame original
        años: lista de enteros, por ejemplo [2023, 2024]
        categorias: lista de strings, por ejemplo ["Tecnologia"]
        regiones: lista de strings, por ejemplo ["Central"]

    Retorna un DataFrame filtrado.
    """
    resultado = df.copy()
    if años:
        resultado = resultado[resultado["Año"].isin(años)]
    if categorias:
        resultado = resultado[resultado["Categoria"].isin(categorias)]
    if regiones:
        resultado = resultado[resultado["Region"].isin(regiones)]
    return resultado


def obtener_opciones(df: pd.DataFrame) -> dict:
    """
    Retorna un diccionario con las opciones unicas para los filtros.

    Llaves: "años", "categorias", "regiones"
    Cada una contiene una lista ordenada.
    """
    return {
        "años": sorted(df["Año"].unique().tolist()),
        "categorias": sorted(df["Categoria"].unique().tolist()),
        "regiones": sorted(df["Region"].unique().tolist()),
    }
# =============================================================================
# PASO 1: Configurar la pagina y cargar los datos
# =============================================================================
st.set_page_config(page_title="Dashboard SuperTienda CR", layout="wide")

df = pd.read_csv("supertienda_cr.csv")

df["Fecha_Orden"] = pd.to_datetime(df["Fecha_Orden"])
df["Año"] = df["Fecha_Orden"].dt.year

# BITACORA — Paso 1
# Antes: Entiendo que cargar un archivo CSV es importar una tabla de datos
# a Python para poder leerla, analizarla y usarla en el dashboard de streamlit. Si he trabajado
# antes con archivos CSV de manera sencilla.
#
# Despues: Al ejecutar streamlit run app.py se abre una aplicacion web loca
# en el navegador. Ahí se ve el dashboard con la informacion en la que he trabajado.

# =============================================================================
# PASO 2: Titulo y resumen general (KPIs)
# =============================================================================

st.title("Dashboard de Ventas - SuperTienda CR")

resumen = calcular_resumen(df)

col1, col2, col3 = st.columns(3)

col1.metric("Ventas Totales", f"${resumen['ventas']:,.0f}")
col2.metric("Ganancia Total", f"${resumen['ganancia']:,.0f}")
col3.metric("Ordenes", resumen["ordenes"])

# BITACORA — Paso 2
# Antes: Un KPI es un indicador clave de desempeño que sirve para medir
# resultados importantes dentro de un negocio o proceso.
#
# Despues: La f antes de las comillas indica que es una f-string y permite
# insertar variables dentro del texto. Si se quita :,.0f, el numero ya no
# se muestra con separador de miles ni redondeado a cero decimales.

# =============================================================================
# PASO 3: Grafico de ventas por mes
# =============================================================================
datos_mes = ventas_por_mes(df)

st.subheader("Ventas por Mes")

st.line_chart(datos_mes, x="Año_Mes", y="Ventas")

# BITACORA — Paso 3
# Antes: Un grafico de linea sirve para mostrar cambios o tendencias a lo largo
# del tiempo. Lo usaria cuando necesito comparar meses, años o periodos.
#
# Despues: El grafico permite observar si hay meses con mayores o menores ventas
# y ayuda a identificar patrones en el comportamiento de los datos.
#
# =============================================================================
# PASO 4: Graficos de barras por categoria y por region
# =============================================================================

izq, der = st.columns(2)

with izq:
    datos_cat = ventas_por_categoria(df)
    st.subheader("Ventas por Categoria")
    st.bar_chart(datos_cat, x="Categoria", y="Ventas")

with der:
    datos_reg = ventas_por_region(df)
    st.subheader("Ventas por Region")
    st.bar_chart(datos_reg, x="Region", y="Ventas")

# BITACORA — Paso 4
# Antes: El grafico de barras sirve para comparar categorias o grupos, mientras
# que el grafico de linea sirve para mostrar tendencias en el tiempo.
#
# Despues: El grafico deja ver cual categoria vende mas y tambien permite
# comparar facilmente el comportamiento por region.
#
# =============================================================================
# PASO 5: Tabla de datos
# =============================================================================
st.subheader("Tabla de Datos")

st.dataframe(df, use_container_width=True, hide_index=True)

# BITACORA — Paso 5
# Antes: Mostrar los datos crudos en un dashboard sirve para revisar detalles,
# validar la informacion y explorar registros individuales.
#
# Despues: Al hacer clic en el encabezado de una columna, la tabla puede
# ordenarse. Eso ayuda a encontrar rapidamente valores altos, bajos o datos
# especificos.
#
# =============================================================================
# PASO 6: Filtros en el sidebar
# =============================================================================
st.sidebar.header("Filtros")

opciones = obtener_opciones(df)

años_sel = st.sidebar.multiselect("Año", opciones["años"])
cats_sel = st.sidebar.multiselect("Categoria", opciones["categorias"])
regs_sel = st.sidebar.multiselect("Region", opciones["regiones"])

df_filtrado = filtrar_datos(
    df,
    años=años_sel or None,
    categorias=cats_sel or None,
    regiones=regs_sel or None,
)

# BITACORA — Paso 6
# Antes: Los filtros deben ir antes de los graficos porque primero se necesita
# definir que datos se van a mostrar. Si van despues, los graficos usarian
# el DataFrame original y no cambiarian.
#
# Despues: Al seleccionar un año, categoria o region, el dashboard debe
# actualizar metricas, graficos y tabla con los datos filtrados.
#
# Reflexion final: Lo mas dificil fue comprender el orden del codigo y como
# conectar los filtros con todo el dashboard. Lo que mas me gusto fue ver
# que la informacion cambia de forma interactiva. Un dashboard se puede
# aplicar en ventas, inventarios, educacion o finanzas.