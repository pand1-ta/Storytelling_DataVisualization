"""
app.py — Dashboard Streamlit
"Latinoamérica: ¿Quién creció limpio?"
Pregunta narrativa: ¿Qué países avanzaron más en energía limpia sin sacrificar
crecimiento económico? (América Latina, 2000–2022)

Paleta elegida: Paleta 1 — Sostenibilidad (Coolors)
  #264653 — verde oscuro     → fondo de cabecera y elementos estructurales
  #2a9d8f — verde agua       → color primario (dato principal: renovables)
  #e9c46a — amarillo dorado  → acento narrativo (hallazgo clave)
  #e76f51 — terracota        → alerta / fósiles / rezago
  #6c757d — gris neutro      → datos de contexto y secundarios

Decisión de color documentada:
  - Verde agua (#2a9d8f): energía limpia, crecimiento positivo, avance.
  - Amarillo dorado (#e9c46a): tensión narrativa — países que solo crecieron
    económicamente sin limpiar su matriz.
  - Terracota (#e76f51): urgencia — alta dependencia fósil o retroceso renovable.
  - Gris (#6c757d): países de contexto no protagonistas de la historia.
  - Nunca más de cuatro colores activos en una misma vista.
"""

# =============================================================================
# LIBRERÍAS
# =============================================================================
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

# =============================================================================
# CONFIGURACIÓN DE PÁGINA
# =============================================================================
st.set_page_config(
    page_title="Latinoamérica: ¿Quién creció limpio?",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =============================================================================
# PALETA DE COLORES (Paleta 1 — Sostenibilidad)
# =============================================================================
COLOR_PRIMARY   = "#2a9d8f"   # verde agua  → renovables / avance
COLOR_ACCENT    = "#e9c46a"   # dorado      → hallazgo / tensión económica
COLOR_ALERT     = "#e76f51"   # terracota   → fósiles / rezago
COLOR_DARK      = "#264653"   # verde oscuro → fondo estructura
COLOR_GRAY      = "#9aabb0"   # gris suave  → contexto / secundario
COLOR_BG        = "#f4f9f8"   # fondo claro

# =============================================================================
# CSS PERSONALIZADO
# =============================================================================
st.markdown(f"""
<style>
  /* Fuente y fondo general */
  html, body, [class*="css"] {{
    font-family: 'Inter', 'Segoe UI', sans-serif;
    background-color: {COLOR_BG};
  }}

  /* Cabecera hero */
  .hero {{
    background: linear-gradient(135deg, {COLOR_DARK} 0%, #1a3a45 100%);
    border-radius: 12px;
    padding: 2.2rem 2.5rem 1.8rem;
    margin-bottom: 0.5rem;
  }}
  .hero h1 {{
    color: #ffffff;
    font-size: 2rem;
    font-weight: 700;
    line-height: 1.25;
    margin: 0 0 0.5rem;
    letter-spacing: -0.02em;
  }}
  .hero p {{
    color: {COLOR_PRIMARY};
    font-size: 1rem;
    margin: 0;
    opacity: 0.95;
  }}

  /* Tarjetas KPI */
  .kpi-row {{
    display: flex;
    gap: 1rem;
    margin: 1.2rem 0;
  }}
  .kpi-card {{
    background: white;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    flex: 1;
    border-left: 4px solid {COLOR_PRIMARY};
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  }}
  .kpi-card.alert {{ border-left-color: {COLOR_ALERT}; }}
  .kpi-card.accent {{ border-left-color: {COLOR_ACCENT}; }}
  .kpi-label {{
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #6b7280;
    margin-bottom: 0.25rem;
  }}
  .kpi-value {{
    font-size: 1.8rem;
    font-weight: 700;
    color: {COLOR_DARK};
    line-height: 1;
  }}
  .kpi-sub {{
    font-size: 0.78rem;
    color: #9ca3af;
    margin-top: 0.2rem;
  }}

  /* Títulos de sección */
  .section-label {{
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: {COLOR_PRIMARY};
    margin: 0 0 0.3rem;
  }}
  .section-title {{
    font-size: 1.15rem;
    font-weight: 700;
    color: {COLOR_DARK};
    margin: 0 0 0.15rem;
  }}
  .section-sub {{
    font-size: 0.85rem;
    color: #6b7280;
    margin: 0 0 1rem;
  }}

  /* Separador */
  .divider {{
    border: none;
    border-top: 1px solid #e5e7eb;
    margin: 1.8rem 0;
  }}

  /* Nota de pie */
  .footnote {{
    font-size: 0.72rem;
    color: #9ca3af;
    margin-top: 0.5rem;
  }}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# CARGA Y PREPARACIÓN DE DATOS
# =============================================================================
@st.cache_data
def cargar_datos():
    """
    Lee el CSV depurado y calcula métricas derivadas necesarias para los
    tres gráficos. No hardcodea ningún valor numérico: todo se computa
    desde el DataFrame.
    """
    # Ruta relativa al CSV dentro del repo (src/ junto a app.py en raíz)
    ruta = os.path.join(os.path.dirname(__file__), "src", "latam_energia_limpio.csv")
    df = pd.read_csv(ruta)

    # ── Métricas derivadas para el scatter (Gráfico 1) ──────────────────
    pivot = df[df["year"].isin([2000, 2022])].pivot_table(
        index="country",
        columns="year",
        values=["renewables_share_elec", "gdp_per_capita", "carbon_intensity_elec"]
    )
    pivot.columns = ["_".join(map(str, c)) for c in pivot.columns]
    pivot = pivot.dropna().reset_index()

    pivot["delta_renew_pp"]  = (
        pivot["renewables_share_elec_2022"] - pivot["renewables_share_elec_2000"]
    )
    pivot["delta_gdp_pct"] = (
        (pivot["gdp_per_capita_2022"] - pivot["gdp_per_capita_2000"])
        / pivot["gdp_per_capita_2000"] * 100
    )
    pivot["renew_2022"] = pivot["renewables_share_elec_2022"]

    # Clasificación narrativa en cuatro cuadrantes
    mediana_renew = pivot["delta_renew_pp"].median()
    mediana_gdp   = pivot["delta_gdp_pct"].median()

    def clasificar(row):
        r = row["delta_renew_pp"] > 0       # avanzó en renovables
        g = row["delta_gdp_pct"]  > mediana_gdp  # sobre mediana de crecimiento
        if r and g:
            return "Avanzó limpio y creció"
        elif r and not g:
            return "Avanzó limpio, menor crecimiento"
        elif not r and g:
            return "Creció, pero no limpió su matriz"
        else:
            return "Retrocedió en renovables y creció poco"

    pivot["cuadrante"] = pivot.apply(clasificar, axis=1)

    # ── Datos para el gráfico de líneas (Gráfico 2) ─────────────────────
    serie_temporal = df[["country", "year", "renewables_share_elec",
                          "gdp_per_capita", "carbon_intensity_elec"]].copy()

    # ── Datos para el heatmap (Gráfico 3) ───────────────────────────────
    heatmap_df = df[["country", "year",
                     "renewables_share_elec", "fossil_share_elec",
                     "carbon_intensity_elec"]].copy()

    return df, pivot, serie_temporal, heatmap_df


df, pivot, serie_temporal, heatmap_df = cargar_datos()


# =============================================================================
# CABECERA HERO
# =============================================================================
st.markdown("""
<div class="hero">
  <h1>Latinoamérica: ¿Quién creció limpio?</h1>
  <p>
    22 países · 2000–2022 · Energía renovable vs. crecimiento económico
    &nbsp;|&nbsp; Fuente: Our World in Data — OWID Energy Dataset
  </p>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# KPIs NARRATIVOS
# =============================================================================
# Calculados 100% desde datos, sin valores hardcodeados
anio_ref = 2022
df22 = df[df["year"] == anio_ref]

n_paises_alto_renov = int((df22["renewables_share_elec"] >= 50).sum())
pais_lider_renov    = df22.loc[df22["renewables_share_elec"].idxmax(), "country"]
renov_lider         = df22["renewables_share_elec"].max()

winners = pivot[
    (pivot["delta_renew_pp"] > 0) & (pivot["delta_gdp_pct"] > pivot["delta_gdp_pct"].median())
]
n_winners = len(winners)

pais_mayor_delta = pivot.loc[pivot["delta_renew_pp"].idxmax(), "country"]
max_delta        = pivot["delta_renew_pp"].max()

st.markdown(f"""
<div class="kpi-row">
  <div class="kpi-card">
    <div class="kpi-label">Países con &gt;50% renovable en 2022</div>
    <div class="kpi-value">{n_paises_alto_renov}</div>
    <div class="kpi-sub">de 22 países analizados</div>
  </div>
  <div class="kpi-card accent">
    <div class="kpi-label">Países que crecieron limpio</div>
    <div class="kpi-value">{n_winners}</div>
    <div class="kpi-sub">avanzaron en renovables Y en PIB per cápita</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Mayor avance renovable 2000→2022</div>
    <div class="kpi-value">{pais_mayor_delta}</div>
    <div class="kpi-sub">+{max_delta:.1f} pp en participación eléctrica renovable</div>
  </div>
  <div class="kpi-card alert">
    <div class="kpi-label">Líder renovable en 2022</div>
    <div class="kpi-value">{pais_lider_renov}</div>
    <div class="kpi-sub">{renov_lider:.0f}% de su electricidad es renovable</div>
  </div>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# FILTRO INTERACTIVO (variante para grupos que terminen antes)
# Propósito narrativo: permite al usuario identificar si su país de interés
# fue un caso de éxito o una promesa incumplida.
# =============================================================================
with st.expander("🔍  Filtrar países para los gráficos de tendencia", expanded=False):
    todos_paises = sorted(df["country"].unique())
    paises_sel = st.multiselect(
        "Selecciona los países a comparar (aplica al Gráfico 2 y 3):",
        options=todos_paises,
        default=["Chile", "Nicaragua", "El Salvador", "Peru", "Mexico", "Brazil",
                 "Costa Rica", "Uruguay", "Argentina"],
        help="Compara trayectorias específicas sin perder el contexto regional."
    )
    if not paises_sel:
        paises_sel = todos_paises

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# =============================================================================
# GRÁFICO 1 — SCATTER: El mapa de los ganadores y rezagados
# Posición: primera, porque responde directamente la pregunta narrativa.
# Mensaje: no todos los que crecieron económicamente limpiaron su matriz,
#          y viceversa. Pocos lograron ambas cosas.
# =============================================================================
st.markdown("""
<div class="section-label">Visualización 1 — Posicionamiento regional</div>
<div class="section-title">¿Quiénes lo lograron? El doble desafío: más renovables <em>y</em> más PIB</div>
<div class="section-sub">
  Variación en puntos porcentuales de electricidad renovable (eje Y) vs. crecimiento del PIB
  per cápita (eje X) entre 2000 y 2022. El tamaño del círculo indica la participación
  renovable alcanzada en 2022.
</div>
""", unsafe_allow_html=True)

COLORES_CUADRANTE = {
    "Avanzó limpio y creció":               COLOR_PRIMARY,
    "Avanzó limpio, menor crecimiento":     COLOR_ACCENT,
    "Creció, pero no limpió su matriz":     COLOR_ALERT,
    "Retrocedió en renovables y creció poco": COLOR_GRAY,
}

fig1 = go.Figure()

for cuadrante, color in COLORES_CUADRANTE.items():
    subset = pivot[pivot["cuadrante"] == cuadrante]
    if subset.empty:
        continue
    fig1.add_trace(go.Scatter(
        x=subset["delta_gdp_pct"],
        y=subset["delta_renew_pp"],
        mode="markers+text",
        name=cuadrante,
        marker=dict(
            size=subset["renew_2022"] / 3 + 10,
            color=color,
            opacity=0.88,
            line=dict(width=1.5, color="white"),
        ),
        text=subset["country"],
        textposition="top center",
        textfont=dict(size=11, color=COLOR_DARK),
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Δ Renovables: %{y:+.1f} pp<br>"
            "Δ PIB per cápita: %{x:+.1f}%<br>"
            "Renovables 2022: %{marker.size:.0f}%<extra></extra>"
        ),
        customdata=subset["renew_2022"],
    ))

# Líneas de referencia en cero
fig1.add_hline(y=0, line_dash="dot", line_color="#cbd5e0", line_width=1.2)
fig1.add_vline(x=pivot["delta_gdp_pct"].median(), line_dash="dot",
               line_color="#cbd5e0", line_width=1.2)

# Etiquetas de cuadrante
mediana_gdp_val = pivot["delta_gdp_pct"].median()
y_max = pivot["delta_renew_pp"].max()
y_min = pivot["delta_renew_pp"].min()
x_max = pivot["delta_gdp_pct"].max()

fig1.add_annotation(
    x=x_max * 0.95, y=y_max * 0.92,
    text="✅ Crecieron limpio",
    showarrow=False,
    font=dict(size=11, color=COLOR_PRIMARY, family="Inter"),
    bgcolor="rgba(42,157,143,0.1)",
    bordercolor=COLOR_PRIMARY,
    borderwidth=1,
    borderpad=5,
    xanchor="right",
)
fig1.add_annotation(
    x=x_max * 0.95, y=y_min * 0.85,
    text="⚠️ Crecieron sin limpiar",
    showarrow=False,
    font=dict(size=11, color=COLOR_ALERT, family="Inter"),
    bgcolor="rgba(231,111,81,0.1)",
    bordercolor=COLOR_ALERT,
    borderwidth=1,
    borderpad=5,
    xanchor="right",
)

fig1.update_layout(
    height=500,
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(family="Inter", color=COLOR_DARK),
    xaxis=dict(
        title="Crecimiento PIB per cápita 2000→2022 (%)",
        gridcolor="#f0f4f3",
        zeroline=False,
        ticksuffix="%",
    ),
    yaxis=dict(
        title="Δ Participación renovable en electricidad (pp)",
        gridcolor="#f0f4f3",
        zeroline=False,
        ticksuffix=" pp",
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.28,
        xanchor="center",
        x=0.5,
        font=dict(size=11),
        bgcolor="rgba(255,255,255,0)",
    ),
    margin=dict(t=20, b=80, l=60, r=20),
)

st.plotly_chart(fig1, use_container_width=True)
st.markdown(
    '<p class="footnote">Nota: la línea vertical punteada marca la mediana regional de crecimiento económico. '
    'El tamaño del círculo es proporcional al porcentaje de electricidad renovable alcanzado en 2022.</p>',
    unsafe_allow_html=True
)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# =============================================================================
# GRÁFICO 2 — LÍNEAS: Las trayectorias que cuentan la historia
# Posición: segunda, porque muestra el "cómo llegaron" a esa posición.
# Mensaje: el avance no fue lineal ni simultáneo. Nicaragua y El Salvador
#          transformaron su matriz en menos de una década.
# =============================================================================
st.markdown("""
<div class="section-label">Visualización 2 — Trayectorias 2000–2022</div>
<div class="section-title">El camino importa: ¿cuándo y cómo limpió su matriz cada país?</div>
<div class="section-sub">
  Evolución de la participación de energía renovable en la generación eléctrica por año.
  Las transformaciones más rápidas ocurrieron entre 2012 y 2020.
</div>
""", unsafe_allow_html=True)

df_line = serie_temporal[serie_temporal["country"].isin(paises_sel)].copy()

# Identificar los top 3 mejoradores dentro de la selección actual
top_mejoradores = (
    pivot[pivot["country"].isin(paises_sel)]
    .nlargest(3, "delta_renew_pp")["country"]
    .tolist()
)

fig2 = go.Figure()

for pais in sorted(df_line["country"].unique()):
    datos_pais = df_line[df_line["country"] == pais].sort_values("year")
    es_protagonista = pais in top_mejoradores

    fig2.add_trace(go.Scatter(
        x=datos_pais["year"],
        y=datos_pais["renewables_share_elec"],
        mode="lines",
        name=pais,
        line=dict(
            width=2.5 if es_protagonista else 1.2,
            color=COLOR_PRIMARY if es_protagonista else COLOR_GRAY,
            dash="solid",
        ),
        opacity=1.0 if es_protagonista else 0.45,
        hovertemplate=(
            f"<b>{pais}</b><br>"
            "Año: %{x}<br>"
            "Renovables: %{y:.1f}%<extra></extra>"
        ),
    ))

# Anotación narrativa del hallazgo principal
if "Nicaragua" in paises_sel:
    nic_2012 = df_line[(df_line["country"] == "Nicaragua") & (df_line["year"] == 2012)]
    nic_2022 = df_line[(df_line["country"] == "Nicaragua") & (df_line["year"] == 2022)]
    if not nic_2012.empty and not nic_2022.empty:
        delta_nic = float(nic_2022["renewables_share_elec"].values[0]) - float(nic_2012["renewables_share_elec"].values[0])
        fig2.add_annotation(
            x=2017, y=float(nic_2022["renewables_share_elec"].values[0]) + 6,
            text=f"Nicaragua: +{delta_nic:.0f} pp en 10 años",
            showarrow=True,
            arrowhead=2,
            arrowcolor=COLOR_PRIMARY,
            font=dict(size=11, color=COLOR_PRIMARY),
            bgcolor="rgba(42,157,143,0.12)",
            bordercolor=COLOR_PRIMARY,
            borderwidth=1,
            borderpad=4,
            ax=-60, ay=-30,
        )

fig2.update_layout(
    height=420,
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(family="Inter", color=COLOR_DARK),
    xaxis=dict(
        title="Año",
        gridcolor="#f0f4f3",
        dtick=2,
    ),
    yaxis=dict(
        title="Renovables en electricidad (%)",
        gridcolor="#f0f4f3",
        range=[-5, 110],
        ticksuffix="%",
    ),
    legend=dict(
        orientation="v",
        x=1.02, y=1,
        font=dict(size=10),
    ),
    margin=dict(t=20, b=50, l=60, r=140),
    hovermode="x unified",
)

st.plotly_chart(fig2, use_container_width=True)
st.markdown(
    '<p class="footnote">Las líneas resaltadas corresponden a los tres países con mayor avance '
    'renovable dentro de la selección actual. Ajusta el filtro superior para comparar otros países.</p>',
    unsafe_allow_html=True
)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# =============================================================================
# GRÁFICO 3 — BARRAS HORIZONTALES APILADAS: La deuda fósil al cierre
# Posición: tercera, cierra la historia mostrando quién sigue dependiendo
#           de combustibles fósiles en 2022 — la deuda pendiente.
# Mensaje: el avance en renovables no es uniforme. Hay países que en 2022
#          aún generan más del 80% de su electricidad con fósiles.
# =============================================================================
st.markdown("""
<div class="section-label">Visualización 3 — Estado al cierre del período (2022)</div>
<div class="section-title">La deuda pendiente: ¿cuánto fósil queda en la matriz eléctrica?</div>
<div class="section-sub">
  Composición de la generación eléctrica en 2022. Cada barra suma 100%.
  Los países están ordenados de mayor a menor participación renovable.
</div>
""", unsafe_allow_html=True)

df_bar = heatmap_df[
    (heatmap_df["year"] == 2022) &
    (heatmap_df["country"].isin(paises_sel))
].copy()

# Calcular la parte "otra" para que sumen 100%
df_bar["otra"] = (100
                  - df_bar["renewables_share_elec"].clip(0, 100)
                  - df_bar["fossil_share_elec"].clip(0, 100)).clip(lower=0)

df_bar = df_bar.sort_values("renewables_share_elec", ascending=True)

fig3 = go.Figure()

fig3.add_trace(go.Bar(
    name="Renovables",
    y=df_bar["country"],
    x=df_bar["renewables_share_elec"],
    orientation="h",
    marker_color=COLOR_PRIMARY,
    hovertemplate="<b>%{y}</b><br>Renovables: %{x:.1f}%<extra></extra>",
))
fig3.add_trace(go.Bar(
    name="Fósiles",
    y=df_bar["country"],
    x=df_bar["fossil_share_elec"],
    orientation="h",
    marker_color=COLOR_ALERT,
    hovertemplate="<b>%{y}</b><br>Fósiles: %{x:.1f}%<extra></extra>",
))
fig3.add_trace(go.Bar(
    name="Nuclear / Otra",
    y=df_bar["country"],
    x=df_bar["otra"],
    orientation="h",
    marker_color=COLOR_GRAY,
    hovertemplate="<b>%{y}</b><br>Nuclear u otro: %{x:.1f}%<extra></extra>",
))

# Anotación del hallazgo narrativo principal del gráfico
# x se posiciona en el centro de la barra fósil, que empieza donde termina la renovable
if not df_bar.empty:
    pais_mas_fosil_sel = df_bar.loc[df_bar["fossil_share_elec"].idxmax()]
    renov_del_pais = float(pais_mas_fosil_sel["renewables_share_elec"])
    fosil_del_pais = float(pais_mas_fosil_sel["fossil_share_elec"])
    x_centro_fosil = renov_del_pais + fosil_del_pais / 2
    fig3.add_annotation(
        x=x_centro_fosil,
        y=pais_mas_fosil_sel["country"],
        text=f"{fosil_del_pais:.0f}% fósil",
        showarrow=False,
        font=dict(size=10, color="white", family="Inter"),
        xanchor="center",
        yanchor="middle",
    )

fig3.update_layout(
    barmode="stack",
    # Altura dinámica + margen inferior generoso para separar leyenda del eje X
    height=max(380, len(df_bar) * 40 + 120),
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(family="Inter", color=COLOR_DARK),
    xaxis=dict(
        # Sin título de eje: la descripción ya está en el subtítulo de sección
        title=None,
        range=[0, 100],
        gridcolor="#f0f4f3",
        ticksuffix="%",
        tickfont=dict(size=11),
    ),
    yaxis=dict(
        title="",
        gridcolor="#f0f4f3",
        tickfont=dict(size=11),
    ),
    legend=dict(
        # Leyenda encima del gráfico para evitar colisión con el eje X
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0,
        font=dict(size=11),
        bgcolor="rgba(255,255,255,0)",
    ),
    margin=dict(t=50, b=40, l=140, r=20),
)

st.plotly_chart(fig3, use_container_width=True)
st.markdown(
    '<p class="footnote">"Nuclear / Otra" incluye energía nuclear, biocombustibles y fuentes no '
    'clasificadas en las categorías principales del dataset.</p>',
    unsafe_allow_html=True
)


# =============================================================================
# PIE DE PÁGINA
# =============================================================================
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown(f"""
<p class="footnote" style="text-align:center;">
  Fuente: Our World in Data — OWID Energy Dataset (owid-energy-data.csv) · 
  Filtro: América Latina, 2000–2022 · 
  Paleta: Coolors "Sostenibilidad" (#264653 · #2a9d8f · #e9c46a · #e76f51) ·
  Data Visualization — 8vo ciclo
</p>
""", unsafe_allow_html=True)