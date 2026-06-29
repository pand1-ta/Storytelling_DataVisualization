# Latinoamérica: ¿Quién creció limpio?

Dashboard narrativo desarrollado para el curso **Data Visualization — 8vo ciclo**.
Responde la pregunta: *¿Qué países de América Latina avanzaron más en energía limpia sin sacrificar crecimiento económico?*

> 🔗 **Dashboard en vivo:** `https://storytellingdatavisualization-xnhxdpnyqhrfgdk3ichsfy.streamlit.app/`

---

## Contexto

Los estudiantes asumen el rol de consultores de datos contratados por una ONG internacional que necesita presentar ante donantes el estado del acceso a energía limpia en América Latina. Este dashboard es la entrega: un relato visual con datos reales del período 2000–2022.

---

## Estructura del repositorio

```
dv-grupo[N]-energia-latam/
├── data/
│   └── owid-energy-data.csv          # Dataset original — Our World in Data
├── src/
│   ├── limpieza_energia_latam.py     # Pipeline de limpieza documentado
│   └── latam_energia_limpio.csv      # Dataset depurado (506 filas × 18 cols)
├── app.py                            # Aplicación Streamlit (entry point)
├── requirements.txt                  # Dependencias
├── .gitattributes                    # Normalización de saltos de línea
└── README.md
```

---

## Dataset

**Fuente:** [Our World in Data — World Energy Consumption](https://ourworldindata.org/energy)  
**Archivo original:** `owid-energy-data.csv` (~4 MB, ~190 variables, 314 países, 1900–2025)  
**Filtro aplicado:** 22 países de América Latina, años 2000–2022  
**Dataset depurado:** 506 filas × 18 columnas, 0 valores nulos en variables clave

### Variables conservadas

| Variable | Descripción | Rol en el análisis |
|---|---|---|
| `country` / `year` | Identificadores | Clave del dataset |
| `gdp` / `population` | Economía bruta | Base para calcular PIB per cápita |
| `gdp_per_capita` | PIB per cápita (derivada) | Eje de crecimiento económico |
| `renewables_share_elec` | % electricidad renovable | Indicador central de energía limpia |
| `fossil_share_elec` | % electricidad fósil | Contraparte / deuda pendiente |
| `solar_share_elec` / `wind_share_elec` | Renovables nuevas | Avance tecnológico reciente |
| `hydro_share_elec` | Hidroeléctrica | Base histórica renovable |
| `carbon_intensity_elec` | gCO₂/kWh generado | Calidad ambiental de la matriz |
| `greenhouse_gas_emissions` | Emisiones totales | Impacto absoluto |
| `energy_per_capita` | Consumo energético/habitante | Eficiencia energética |

---

## Storyboard

### Pregunta narrativa central
> **¿Qué países de América Latina avanzaron más en energía limpia sin sacrificar crecimiento económico?**

### Flujo narrativo de las visualizaciones

**Gráfico 1 — Scatter de cuadrantes** *(primera posición)*  
Responde directamente la pregunta: posiciona a los 22 países según cuánto avanzaron en renovables (eje Y) y cuánto creció su PIB per cápita (eje X) entre 2000 y 2022. El cuadrante superior derecho contiene a los países que lograron ambas metas simultáneamente.

**Gráfico 2 — Líneas temporales** *(segunda posición)*  
Responde el "¿cómo llegaron?": muestra las trayectorias anuales de renovables por país. Evidencia que el avance no fue lineal ni simultáneo — Nicaragua y El Salvador transformaron su matriz en menos de una década (2012–2022).

**Gráfico 3 — Barras apiladas horizontales** *(tercera posición, cierre)*  
Cierra la historia con el estado actual: ¿cuánto fósil queda en 2022? Muestra la composición completa de la matriz eléctrica ordenada de mayor a menor renovable. Plantea la pregunta implícita: ¿quiénes tienen aún una deuda pendiente?

### Conexión narrativa entre gráficos
El scatter identifica a los protagonistas → las líneas muestran su trayectoria → las barras revelan cuánto camino queda por recorrer.

---

## Paleta de colores — Paleta 1: Sostenibilidad

Fuente: [Coolors.co](https://coolors.co/palette/264653-2a9d8f-e9c46a-f4a261-e76f51)

| Color | Hex | Intención narrativa |
|---|---|---|
| Verde oscuro | `#264653` | Fondo estructural. Autoridad y profundidad — evoca recursos naturales. |
| Verde agua | `#2a9d8f` | **Color primario.** Representa renovables y avance positivo. Es el color de la respuesta correcta a la pregunta. |
| Amarillo dorado | `#e9c46a` | **Acento.** Tensión narrativa: países que crecieron económicamente sin limpiar su matriz. El dorado no es negativo, pero sí incompleto. |
| Terracota | `#e76f51` | **Alerta.** Alta dependencia fósil, retroceso en renovables. Urgencia sin alarmismo. |
| Gris suave | `#9aabb0` | Datos de contexto. Países que no son protagonistas de la historia en esa vista. |

**Regla aplicada:** máximo cuatro colores activos por vista. El gris absorbe el contexto sin competir con el dato principal.

---

## Requisitos técnicos

```
streamlit>=1.32.0
pandas>=2.0.0
plotly>=5.20.0
```

Instalación local:

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Despliegue

El dashboard está desplegado en **Streamlit Community Cloud** desde este repositorio público.

Flujo de despliegue:
1. Repositorio público en GitHub con nombre `dv-grupo[N]-energia-latam`
2. Conectado a [streamlit.io/cloud](https://streamlit.io/cloud)
3. Entry point: `app.py` (raíz del repositorio)
4. Sin variables de entorno requeridas

---

## Criterios de evaluación cubiertos

| Criterio | Implementación |
|---|---|
| Claridad narrativa (30%) | Pregunta única → 3 gráficos con flujo causa–trayectoria–estado |
| Uso intencional del color (25%) | Paleta documentada, cada color con justificación, máx. 4 activos por vista |
| Calidad técnica (20%) | `@st.cache_data`, sin valores hardcodeados, pipeline de limpieza separado |
| Dashboard desplegado (15%) | URL pública en Streamlit Cloud |
| Presentación narrativa (10%) | Storyboard documentado en este README |

---

## Integrante
- Jimena Quintana Noa
