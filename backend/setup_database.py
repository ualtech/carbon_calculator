"""
setup_database.py

Crea (o regenera) la base de datos SQLite carbon_calculator.db a partir de los
CSV de la carpeta data/. Cada parametro (coeficiente de modelo, factor regional,
equivalencia, presupuesto de tokens) lleva su fuente y su fecha de referencia.

Ejecutar desde la raiz del proyecto:
    python -m backend.setup_database
"""
import sqlite3
import csv
import os
from datetime import date

DB_NAME = "carbon_calculator.db"
TOOL_VERSION = "2.0.0"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# ===========================
# CREAR TABLAS
# ===========================
cursor.execute("DROP TABLE IF EXISTS modelos")
cursor.execute("DROP TABLE IF EXISTS factores_region")
cursor.execute("DROP TABLE IF EXISTS equivalencias")
cursor.execute("DROP TABLE IF EXISTS tipos_tarea")
cursor.execute("DROP TABLE IF EXISTS metadata")

cursor.execute("""
CREATE TABLE modelos (
    id_modelo INTEGER PRIMARY KEY,
    nombre_modelo TEXT NOT NULL,
    proveedor TEXT,
    version_modelo TEXT,
    kwh_por_millon_tokens REAL NOT NULL,
    fuente TEXT NOT NULL,
    fecha_referencia TEXT,
    en_caso_estudio INTEGER DEFAULT 0,
    notas TEXT
)
""")

cursor.execute("""
CREATE TABLE factores_region (
    id_region INTEGER PRIMARY KEY,
    nombre_region TEXT NOT NULL,
    intensidad_carbono_kg_kwh REAL NOT NULL,
    anio_referencia INTEGER,
    fuente TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE equivalencias (
    id_equivalencia INTEGER PRIMARY KEY,
    tipo TEXT NOT NULL,
    factor_conversion REAL NOT NULL,
    unidad TEXT,
    fuente TEXT NOT NULL,
    notas TEXT
)
""")

cursor.execute("""
CREATE TABLE tipos_tarea (
    id_tipo INTEGER PRIMARY KEY,
    tipo TEXT NOT NULL UNIQUE,
    etiqueta TEXT,
    tokens_entrada INTEGER NOT NULL,
    tokens_salida INTEGER NOT NULL,
    descripcion TEXT,
    fuente TEXT
)
""")

cursor.execute("""
CREATE TABLE metadata (
    clave TEXT PRIMARY KEY,
    valor TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS consultas_log (
    id_consulta INTEGER PRIMARY KEY,
    fecha_timestamp TEXT,
    id_modelo INTEGER,
    id_region INTEGER,
    tokens_entrada INTEGER,
    tokens_salida INTEGER,
    co2_kg REAL,
    FOREIGN KEY (id_modelo) REFERENCES modelos(id_modelo),
    FOREIGN KEY (id_region) REFERENCES factores_region(id_region)
)
""")
print("Tablas creadas correctamente.")

# ===========================
# POBLAR DESDE CSV
# ===========================
def populate_table(csv_file, table_name):
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"Archivo no encontrado: {csv_file}")
    with open(csv_file, "r", encoding="utf-8-sig") as f:
        dr = csv.DictReader(f, delimiter=';')
        cols = dr.fieldnames
        rows = [tuple(r[c] if r[c] != "" else None for c in cols) for r in dr]
    placeholders = ", ".join(["?"] * len(cols))
    cursor.executemany(
        f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES ({placeholders})", rows
    )
    print(f"Tabla '{table_name}': {len(rows)} filas desde {csv_file}")

populate_table("data/models_data.csv", "modelos")
populate_table("data/regions_data.csv", "factores_region")
populate_table("data/equivalencias.csv", "equivalencias")
populate_table("data/tipos_tarea.csv", "tipos_tarea")

cursor.executemany("INSERT INTO metadata (clave, valor) VALUES (?, ?)", [
    ("tool_version", TOOL_VERSION),
    ("db_build_date", date.today().isoformat()),
    ("db_cutoff_note", "Coeficientes de modelos: Jegham et al. 2025 (arXiv:2505.09598v5, nov-2025) y Google 2025 (arXiv:2508.15734). Factores regionales: CNMC 2026 (datos 2025), Ember 2023 (datos 2022) y Ember 2025 (datos 2024)."),
])

conn.commit()
conn.close()
print(f"Base de datos poblada correctamente (version {TOOL_VERSION}).")
