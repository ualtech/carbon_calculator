from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from backend.calculations import calculate_co2, get_equivalences, tokens_for_task
from backend.database import (get_all_models, get_all_regions, get_model_by_id, get_region_factor,
                              get_region_id, log_calculation, get_all_task_types, get_metadata)
from typing import Optional
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Carbon Calculator API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================
# MODELO DE REQUEST
# ===========================
class CalculationRequest(BaseModel):
    model_id: int
    region: str
    tokens_input: Optional[int] = None
    tokens_output: Optional[int] = None
    task_type: Optional[str] = None  # 'simple' | 'medium' | 'complex' (rellena los tokens si no se indican)

# ===========================
# MODELOS DE REQUEST: COMPARADOR Y SIMULADOR
# ===========================
class CompareScenario(BaseModel):
    model_id: int
    region: str
    tokens_input: Optional[int] = None
    tokens_output: Optional[int] = None
    task_type: Optional[str] = None

class CompareRequest(BaseModel):
    scenario1: CompareScenario
    scenario2: CompareScenario

class Activity(BaseModel):
    name: str
    model_id: int
    tokens_per_student: int
    frequency: str  # daily, weekly, monthly
    weeks: int

class SimulateRequest(BaseModel):
    num_students: int
    activities: List[Activity]
    region: str


# ===========================
# RESOLUCION DE TOKENS (tipo de tarea o entrada directa)
# ===========================
def resolve_tokens(tokens_input, tokens_output, task_type, where=""):
    """Si no se indican tokens, usa el presupuesto documentado del tipo de tarea."""
    if tokens_input is None or tokens_output is None:
        if not task_type:
            raise HTTPException(status_code=400,
                detail=f"Indica tokens_input y tokens_output, o bien task_type{where}")
        try:
            t_in, t_out = tokens_for_task(task_type)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        tokens_input = t_in if tokens_input is None else tokens_input
        tokens_output = t_out if tokens_output is None else tokens_output
    if tokens_input < 0 or tokens_output < 0:
        raise HTTPException(status_code=400, detail=f"Tokens no pueden ser negativos{where}")
    return tokens_input, tokens_output

# ===========================
# ENDPOINTS
# ===========================
@app.get("/")
def root():
    return {"message": "Carbon Calculator API running", "version": get_metadata().get("tool_version")}

@app.get("/version")
def version():
    return get_metadata()

@app.get("/task_types")
def list_task_types():
    try:
        return get_all_task_types()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener tipos de tarea: {str(e)}")

@app.get("/models")
def list_models():
    try:
        models = get_all_models()
        if not models:
            raise HTTPException(status_code=404, detail="No hay modelos disponibles")
        return models
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener modelos: {str(e)}")

@app.get("/regions")
def list_regions():
    try:
        regions = get_all_regions()
        if not regions:
            raise HTTPException(status_code=404, detail="No hay regiones disponibles")
        return regions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener regiones: {str(e)}")

@app.post("/calculate")
def calculate(request: CalculationRequest):
    tokens_input, tokens_output = resolve_tokens(request.tokens_input, request.tokens_output, request.task_type)
    
    model = get_model_by_id(request.model_id)
    if not model:
        raise HTTPException(status_code=404, detail=f"Modelo con id {request.model_id} no encontrado")
    
    factor_region = get_region_factor(request.region)
    if factor_region is None:
        raise HTTPException(status_code=404, detail=f"Región '{request.region}' no encontrada")
    
    try:
        result = calculate_co2(
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            model_id=request.model_id,
            region=request.region
        )
        equivalences = get_equivalences(result["co2_kg"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en cálculo o equivalencias: {str(e)}")

    try:
        log_calculation({
            "fecha_timestamp": datetime.now().isoformat(),
            "id_modelo": request.model_id,
            "id_region": get_region_id(request.region),
            "tokens_entrada": tokens_input,
            "tokens_salida": tokens_output,
            "co2_kg": result["co2_kg"]
        })
    except Exception as e:
        print(f"Warning: error al loguear cálculo: {e}")

    return {
        "calculation": result,
        "equivalences": equivalences
    }

# ===========================
# ENDPOINT COMPARADOR
# ===========================
@app.post("/compare")
def compare(request: CompareRequest):
    results = {}
    for key, scenario in [("scenario1", request.scenario1), ("scenario2", request.scenario2)]:
        t_in, t_out = resolve_tokens(scenario.tokens_input, scenario.tokens_output, scenario.task_type, f" en {key}")
        if not get_model_by_id(scenario.model_id):
            raise HTTPException(status_code=404, detail=f"Modelo id {scenario.model_id} no encontrado en {key}")
        if get_region_factor(scenario.region) is None:
            raise HTTPException(status_code=404, detail=f"Región '{scenario.region}' no encontrada en {key}")

        result = calculate_co2(
            tokens_input=t_in,
            tokens_output=t_out,
            model_id=scenario.model_id,
            region=scenario.region
        )
        result["equivalences"] = get_equivalences(result["co2_kg"])
        results[key] = result

    co2_diff = results["scenario1"]["co2_kg"] - results["scenario2"]["co2_kg"]
    max_co2 = max(results["scenario1"]["co2_kg"], results["scenario2"]["co2_kg"])
    co2_diff_pct = (abs(co2_diff) / max_co2 * 100) if max_co2 != 0 else 0
    results["difference"] = {
        "co2_kg": round(co2_diff, 6),
        "percentage": round(co2_diff_pct, 2)
    }

    return results

# ===========================
# ENDPOINT SIMULADOR
# ===========================
@app.post("/simulate")
def simulate(request: SimulateRequest):
    if request.num_students <= 0:
        raise HTTPException(status_code=400, detail="Número de estudiantes debe ser mayor que 0")
    if get_region_factor(request.region) is None:
        raise HTTPException(status_code=404, detail=f"Región '{request.region}' no encontrada")

    total_co2 = 0
    breakdown = []

    for activity in request.activities:
        if activity.tokens_per_student < 0 or activity.weeks < 1:
            raise HTTPException(status_code=400, detail=f"Tokens o semanas inválidas en actividad '{activity.name}'")
        if not get_model_by_id(activity.model_id):
            raise HTTPException(status_code=404, detail=f"Modelo id {activity.model_id} no encontrado en actividad '{activity.name}'")

        frequency = activity.frequency.lower()

        if frequency == "daily":
            total_events = activity.weeks * 7
        elif frequency == "weekly":
            total_events = activity.weeks
        elif frequency == "monthly":
            total_events = activity.weeks / 4
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Frecuencia inválida en actividad '{activity.name}'. Usa daily, weekly o monthly."
            )

        tokens_total = (
            activity.tokens_per_student
            * request.num_students
            * total_events
        )

        result = calculate_co2(
            tokens_input=int(tokens_total),
            tokens_output=0,
            model_id=activity.model_id,
            region=request.region
        )

        result["co2_kg"] = round(result["co2_kg"], 6)
        total_co2 += result["co2_kg"]

        breakdown.append({
            "activity": activity.name,
            "co2_kg": result["co2_kg"],
            "tokens_total": result["tokens_total"],
            "equivalences": get_equivalences(result["co2_kg"])
        })

        try:
            log_calculation({
                "fecha_timestamp": datetime.now().isoformat(),
                "id_modelo": activity.model_id,
                "id_region": get_region_id(request.region),
                "tokens_entrada": activity.tokens_per_student * request.num_students,
                "tokens_salida": 0,
                "co2_kg": result["co2_kg"]
            })
        except Exception as e:
            print(f"Warning: error al loguear actividad '{activity.name}': {e}")

    return {
        "total_co2_kg": round(total_co2, 6),
        "per_student_co2_kg": round(total_co2 / request.num_students, 6),
        "equivalences": get_equivalences(total_co2),
        "breakdown_by_activity": breakdown
    }