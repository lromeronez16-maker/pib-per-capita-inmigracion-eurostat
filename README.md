# PIB total vs PIB per cápita en la UE (Eurostat)

Este proyecto responde a una pregunta muy concreta: **¿crecer en PIB total es lo mismo que crecer en PIB per cápita?**
Compara la evolución de ambos indicadores para varios países de la UE usando datos abiertos de Eurostat.

## Objetivo

- Descargar series temporales de PIB per cápita (PPS, ajustado por poder adquisitivo) y de crecimiento real del PIB.
- Comparar la evolución de varios países.
- Visualizar la diferencia entre "la economía crece" y "la economía crece más rápido que la población".

## Fuente de datos

- **Eurostat API REST** (JSON-stat), sin necesidad de API key:
  - `tec00114` — PIB per cápita en PPS (índice, UE27=100)
  - `tec00115` — Tasa de crecimiento real del PIB
  - Endpoint base: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{código}?format=JSON&lang=EN`
  - Documentación: https://ec.europa.eu/eurostat/web/main/data/web-services

> ⚠️ Eurostat actualiza y a veces renombra códigos de tabla. Si `fetch_data.py` falla, busca el código actualizado en el [Data Browser de Eurostat](https://ec.europa.eu/eurostat/databrowser/) buscando "GDP per capita" o "Real GDP growth rate".

## Estructura

```
01-pib-vs-pib-per-capita-eurostat/
├── fetch_data.py        # Descarga datos reales desde la API de Eurostat
├── analisis.ipynb        # Notebook con el análisis y las gráficas
├── data/
│   └── sample_pib.csv    # Datos de ejemplo (ilustrativos) para poder ejecutar el notebook sin conexión
└── README.md
```

## Cómo ejecutarlo

```bash
pip install -r ../requirements.txt
python fetch_data.py          # genera data/pib_real.csv con datos actualizados de Eurostat
jupyter notebook analisis.ipynb
```

Si no tienes conexión o la API cambia de estructura, el notebook cae automáticamente en `data/sample_pib.csv` (datos ilustrativos, no oficiales) para que el código y las gráficas sigan funcionando.

## Qué muestra el análisis

1. Evolución del PIB per cápita (PPS) por país.
2. Comparación entre crecimiento del PIB total y crecimiento del PIB per cápita.
3. Ranking de países por PIB per cápita en el último año disponible.

## Posibles ampliaciones

- Añadir la variable de saldo migratorio neto (Eurostat, tabla `migr_imm1ctz` / `tps00019`) y correlacionarla con el crecimiento del PIB per cápita.
- Comparar comunidades autónomas españolas usando datos del INE en vez de países de la UE.
