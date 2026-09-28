import sqlite3

DB_NAME = "carbon_calculator.db"


def get_connection():
    """Devuelve una nueva conexion a la base de datos."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def _fetch_all(query, params=()):
    conn = get_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def _fetch_one(query, params=()):
    conn = get_connection()
    row = conn.execute(query, params).fetchone()
    conn.close()
    return dict(row) if row else None


# ===========================
# MODELOS
# ===========================
def get_all_models():
    return _fetch_all("SELECT * FROM modelos ORDER BY id_modelo")


def get_model_by_id(model_id):
    return _fetch_one("SELECT * FROM modelos WHERE id_modelo = ?", (model_id,))


# ===========================
# REGIONES
# ===========================
def get_region_factor(region_name):
    row = _fetch_one(
        "SELECT intensidad_carbono_kg_kwh FROM factores_region WHERE nombre_region = ?",
        (region_name,),
    )
    return row["intensidad_carbono_kg_kwh"] if row else None


def get_region_id(region_name):
    row = _fetch_one(
        "SELECT id_region FROM factores_region WHERE nombre_region = ?", (region_name,)
    )
    return row["id_region"] if row else None


def get_all_regions():
    return _fetch_all("SELECT * FROM factores_region ORDER BY id_region")


# ===========================
# EQUIVALENCIAS
# ===========================
def get_all_equivalences():
    return _fetch_all("SELECT * FROM equivalencias ORDER BY id_equivalencia")


# ===========================
# TIPOS DE TAREA (presupuestos de tokens)
# ===========================
def get_all_task_types():
    return _fetch_all("SELECT * FROM tipos_tarea ORDER BY id_tipo")


def get_task_type(task_type):
    return _fetch_one("SELECT * FROM tipos_tarea WHERE tipo = ?", (task_type.lower(),))


# ===========================
# METADATA
# ===========================
def get_metadata():
    rows = _fetch_all("SELECT clave, valor FROM metadata")
    return {r["clave"]: r["valor"] for r in rows}


# ===========================
# LOG DE CONSULTAS
# ===========================
def log_calculation(data):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO consultas_log (
            fecha_timestamp, id_modelo, id_region,
            tokens_entrada, tokens_salida, co2_kg
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            data["fecha_timestamp"],
            data["id_modelo"],
            data["id_region"],
            data["tokens_entrada"],
            data["tokens_salida"],
            data["co2_kg"],
        ),
    )
    conn.commit()
    conn.close()
