"""
calculations.py

Logica de calculo de la huella de carbono. No contiene logica de API ni de
interfaz: solo calculos puros reutilizables (los usa la API y el script del
caso de estudio, de modo que ambos producen exactamente los mismos numeros).

Modelo de calculo (Ec. 1 del articulo):

    CO2 (kg) = N_tokens x (E_Mtoken / 1e6) x CI_grid

    N_tokens  : tokens totales procesados (entrada + salida)
    E_Mtoken  : consumo del modelo en kWh por millon de tokens (tabla modelos)
    CI_grid   : intensidad de carbono de la red en kg CO2e/kWh (tabla factores_region)
"""

from backend.database import (
    get_model_by_id,
    get_region_factor,
    get_all_equivalences,
    get_task_type,
)


# =====================================================
# 1. PRESUPUESTO DE TOKENS POR TIPO DE TAREA
# =====================================================

def tokens_for_task(task_type):
    """
    Devuelve el presupuesto de tokens (entrada, salida) asociado a un tipo de
    tarea ('simple', 'medium', 'complex'), tal como esta documentado en la
    tabla tipos_tarea. El usuario puede editar estos valores en la interfaz.
    """
    t = get_task_type(task_type)
    if not t:
        raise ValueError(f"Tipo de tarea no encontrado: {task_type}")
    return t["tokens_entrada"], t["tokens_salida"]


# =====================================================
# 2. CALCULO PRINCIPAL DE CO2
# =====================================================

def calculate_co2(tokens_input, tokens_output, model_id, region):
    """
    Calcula la energia y el CO2 asociados a una interaccion.

    Returns:
        dict con co2_kg, kwh, tokens_total, kwh_por_millon_tokens y
        intensidad_carbono_kg_kwh (los dos parametros aplicados, para
        trazabilidad).
    """
    if tokens_input < 0 or tokens_output < 0:
        raise ValueError("Los tokens no pueden ser negativos")

    model = get_model_by_id(model_id)
    if not model:
        raise ValueError("Modelo no encontrado")

    factor_region = get_region_factor(region)
    if factor_region is None:
        raise ValueError("Region no encontrada")

    tokens_total = tokens_input + tokens_output

    # E_Mtoken esta en kWh por millon de tokens -> normalizar a kWh/token
    kwh = tokens_total * (model["kwh_por_millon_tokens"] / 1_000_000)
    co2_kg = kwh * factor_region

    return {
        "co2_kg": round(co2_kg, 6),
        "kwh": round(kwh, 6),
        "tokens_total": tokens_total,
        "kwh_por_millon_tokens": model["kwh_por_millon_tokens"],
        "intensidad_carbono_kg_kwh": factor_region,
    }


# =====================================================
# 3. EQUIVALENCIAS
# =====================================================

def get_equivalences(co2_kg):
    """
    Convierte kg de CO2 a equivalencias comprensibles usando los factores
    documentados en la tabla equivalencias (factor = unidades por kg CO2).
    """
    if co2_kg < 0:
        raise ValueError("El CO2 no puede ser negativo")

    results = {}
    for eq in get_all_equivalences():
        results[eq["tipo"]] = round(co2_kg * eq["factor_conversion"], 4)
    return results
