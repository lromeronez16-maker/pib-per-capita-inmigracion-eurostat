"""
fetch_data.py
Descarga datos reales de la API de Eurostat (formato JSON-stat) sobre:
  - PIB per cápita en PPS                          (tec00114)
  - Tasa de crecimiento real del PIB                (tec00115)
  - Población a 1 de enero                          (tps00001)
  - Cambio de población: tasas brutas, incluido
    el saldo migratorio neto                        (tps00019)

No requiere API key. Genera data/pib_real.csv y data/poblacion_migracion_real.csv

Uso:
    python fetch_data.py
"""

import itertools
import requests
import pandas as pd

BASE_URL = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"

# Países a comparar (código ISO de 2 letras que usa Eurostat)
PAISES = ["ES", "DE", "FR", "IT", "PL", "EU27_2020"]


def descargar_tabla(codigo_tabla: str, paises: list) -> pd.DataFrame:
    """Descarga una tabla de Eurostat en formato JSON-stat y la convierte a DataFrame largo."""
    params = {"format": "JSON", "lang": "EN", "geo": paises}
    url = f"{BASE_URL}/{codigo_tabla}"

    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    dims = data["dimension"]
    dim_ids = data["id"]

    # Índices -> etiquetas para cada dimensión
    dim_labels = {}
    for dim in dim_ids:
        cat = dims[dim]["category"]["index"]
        if isinstance(cat, dict):
            ordered = sorted(cat.items(), key=lambda kv: kv[1])
            dim_labels[dim] = [k for k, _ in ordered]
        else:
            dim_labels[dim] = cat

    combos = list(itertools.product(*[dim_labels[d] for d in dim_ids]))

    values = data["value"]
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
    # --- PIB total y PIB per cápita ---
    frames_pib = []
    for tabla in ["tec00114", "tec00115"]:
        try:
            print(f"Descargando {tabla}...")
            frames_pib.append(descargar_tabla(tabla, PAISES))
        except Exception as e:
            print(f"⚠️  No se pudo descargar {tabla}: {e}")

    if frames_pib:
        pd.concat(frames_pib, ignore_index=True).to_csv("data/pib_real.csv", index=False)
        print("✅ Guardado en data/pib_real.csv")

    # --- Población y saldo migratorio ---
    frames_demo = []
    for tabla in ["tps00001", "tps00019"]:
        try:
            print(f"Descargando {tabla}...")
            frames_demo.append(descargar_tabla(tabla, PAISES))
        except Exception as e:
            print(f"⚠️  No se pudo descargar {tabla}: {e}")

    if frames_demo:
        df_demo = pd.concat(frames_demo, ignore_index=True)
        df_demo.to_csv("data/poblacion_migracion_real.csv", index=False)
        print("✅ Guardado en data/poblacion_migracion_real.csv")
        print("   Nota: la tabla tps00019 incluye varias tasas (cambio total, cambio")
        print("   natural, saldo migratorio neto) en la misma tabla. Filtra por la")
        print("   dimensión correspondiente (revisa la columna 'indic_de' del CSV)")
        print("   para quedarte solo con el saldo migratorio neto.")


if __name__ == "__main__":
    main()
