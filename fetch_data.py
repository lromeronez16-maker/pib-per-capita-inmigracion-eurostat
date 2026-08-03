"""
fetch_data.py
Descarga datos reales de Eurostat (API JSON-stat) sobre:
  - PIB per cápita en PPS (tec00114)
  - Tasa de crecimiento real del PIB (tec00115)

No requiere API key. Genera data/pib_real.csv

Uso:
    python fetch_data.py
"""

import requests
import pandas as pd

BASE_URL = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"

# Países a comparar (código ISO de 2 letras que usa Eurostat)
PAISES = ["ES", "DE", "FR", "IT", "PL", "EU27_2020"]


def descargar_tabla(codigo_tabla: str, paises: list[str]) -> pd.DataFrame:
    """Descarga una tabla de Eurostat en formato JSON-stat y la convierte a DataFrame largo."""
    params = {"format": "JSON", "lang": "EN"}
    url = f"{BASE_URL}/{codigo_tabla}"

    resp = requests.get(url, params={**params, "geo": paises}, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    # JSON-stat: hay que reconstruir las dimensiones a partir de "dimension" y "value"
    dims = data["dimension"]
    dim_ids = data["id"]
    sizes = data["size"]

    # Índices -> etiquetas para cada dimensión
    dim_labels = {}
    for dim in dim_ids:
        cat = dims[dim]["category"]["index"]
        # category.index puede ser dict {label: pos} o lista
        if isinstance(cat, dict):
            ordered = sorted(cat.items(), key=lambda kv: kv[1])
            dim_labels[dim] = [k for k, _ in ordered]
        else:
            dim_labels[dim] = cat

    # Reconstruir todas las combinaciones (producto cartesiano) en el mismo orden que "value"
    import itertools
    combos = list(itertools.product(*[dim_labels[d] for d in dim_ids]))

    values = data["value"]  # dict {posicion_str: valor} en formato JSON-stat 2.0
    rows = []
    for i, combo in enumerate(combos):
        val = values.get(str(i))
        if val is None:
            continue
        row = dict(zip(dim_ids, combo))
        row["value"] = val
        rows.append(row)

    df = pd.DataFrame(rows)
    df["indicador"] = codigo_tabla
    return df


def main():
    frames = []
    for tabla in ["tec00114", "tec00115"]:
        try:
            print(f"Descargando {tabla}...")
            df = descargar_tabla(tabla, PAISES)
            frames.append(df)
        except Exception as e:
            print(f"⚠️  No se pudo descargar {tabla}: {e}")
            print("   Revisa https://ec.europa.eu/eurostat/databrowser/ por si el código cambió.")

    if not frames:
        print("No se descargó ningún dato. Usa data/sample_pib.csv como alternativa.")
        return

    final = pd.concat(frames, ignore_index=True)
    final.to_csv("data/pib_real.csv", index=False)
    print(f"✅ Guardado en data/pib_real.csv ({len(final)} filas)")


if __name__ == "__main__":
    main()
