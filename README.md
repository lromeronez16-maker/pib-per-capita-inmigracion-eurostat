## Sobre mí

**Lorenzo** — Estudiante de ADE (4º curso), UCLM, Ciudad Real

Estudiante de 4º curso del Grado en Administración y Dirección de Empresas (ADE) en la Universidad de Castilla-La Mancha (Ciudad Real). Dentro del grado, eligiendo entre dos itinerarios: **Dirección Económico-Financiera y Fiscal** (con máster en auditoría) y **Economía y Métodos Cuantitativos** (con máster en modelización de datos).

Me he decantado por el itinerario cuantitativo: mejor posicionamiento a largo plazo en un entorno donde el análisis de datos y la IA son cada vez más centrales en economía y finanzas. Mi objetivo es combinar una formación económica sólida con herramientas cuantitativas y de programación de ahí estos proyectos de portfolio.

> Este notebook se ha construido con asistencia de IA (Claude, de Anthropic). Los datos, el planteamiento del análisis y las conclusiones han sido revisados y validados por el autor.
# PIB total vs PIB per cápita en la UE, y el papel de la inmigración

Este proyecto responde a una pregunta muy concreta: **¿crecer en PIB total es lo mismo que crecer en PIB per cápita?** Y, en particular, ¿qué papel juega ahí la inmigración, que suele mencionarse como motor de crecimiento económico?

Compara la evolución de ambos indicadores para varios países de la UE usando datos abiertos de Eurostat, e incorpora población y saldo migratorio neto para explorar esa diferencia con más detalle.

## Objetivo

- Descargar series temporales de PIB per cápita (PPS), crecimiento real del PIB, población y saldo migratorio neto.
- Comparar la evolución de varios países.
- Visualizar la diferencia entre "la economía crece" y "la economía crece más rápido que la población" — y por qué esa distinción importa especialmente cuando se habla de inmigración.

## Fuente de datos

**Eurostat API REST** (JSON-stat), sin necesidad de API key:

| Código | Descripción |
|---|---|
| `tec00114` | PIB per cápita en PPS (índice, UE27 = 100) |
| `tec00115` | Tasa de crecimiento real del PIB |
| `tps00001` | Población a 1 de enero |
| `tps00019` | Cambio de población: tasas brutas, incluido el saldo migratorio neto |

- Endpoint base: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{código}?format=JSON&lang=EN`
- Documentación: https://ec.europa.eu/eurostat/web/main/data/web-services

> ⚠️ Eurostat actualiza y a veces renombra códigos de tabla. Si `fetch_data.py` falla, busca el código actualizado en el [Data Browser de Eurostat](https://ec.europa.eu/eurostat/databrowser/). La tabla `tps00019` incluye varias tasas en un mismo cubo (cambio total, cambio natural, saldo migratorio neto); hay que filtrar por la dimensión correspondiente para quedarse solo con el saldo migratorio.

## Estructura

```
01-pib-vs-pib-per-capita-eurostat/
├── fetch_data.py       # Descarga datos reales desde la API de Eurostat
├── analisis.ipynb        # Notebook con el análisis y las gráficas
├── data/
│   └── sample_pib.csv    # Datos de ejemplo (ilustrativos) para poder ejecutar el notebook sin conexión
└── README.md
```

## Cómo ejecutarlo

```bash
pip install -r ../requirements.txt
python fetch_data.py          # genera data/pib_real.csv y data/poblacion_migracion_real.csv
jupyter notebook analisis.ipynb
```

Si no tienes conexión o la API cambia de estructura, el notebook cae automáticamente en `data/sample_pib.csv` (datos ilustrativos, no oficiales) para que el código y las gráficas sigan funcionando.

## Qué muestra el análisis

1. Evolución del PIB per cápita (PPS) por país.
2. Comparación entre crecimiento del PIB total y crecimiento del PIB per cápita.
3. Comparación entre PIB total, PIB per cápita y crecimiento de la población — el bloque central del proyecto.
4. Relación descriptiva entre saldo migratorio neto y cambio en el PIB per cápita (sin implicar causalidad).
5. Ranking de países por PIB per cápita en el último año disponible.

## Una aclaración importante

Este notebook **no pretende demostrar** que la inmigración mejora o empeora el PIB per cápita — eso requeriría los métodos econométricos descritos en el artículo que acompaña a este proyecto (diferencias en diferencias, variables instrumentales, control de otros factores). Lo que sí muestra, con datos reales, es que PIB total, PIB per cápita y población son tres variables distintas que conviene mirar por separado antes de sacar conclusiones.

## Posibles ampliaciones

- Aplicar un modelo de regresión simple controlando por año y país (efectos fijos) en vez de una correlación descriptiva.
- Añadir más países y más años para robustecer el análisis.
- Comparar comunidades autónomas españolas usando datos del INE en vez de países de la UE.
