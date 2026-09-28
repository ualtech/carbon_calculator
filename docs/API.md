# API Carbon Calculator

## GET /

**Descripción:** endpoint raíz
**Response:**
```json
{"message": "Carbon Calculator API running"}

GET /version
Descripción: versión de la herramienta y fecha de construcción de la base de datos

GET /task_types
Descripción: presupuestos de tokens por tipo de tarea (simple, medium, complex)

GET /models
Descripción: devuelve todos los modelos disponibles (con coeficiente, fuente y fecha de referencia)
 Response 200: lista de modelos
 Response 404: no hay modelos disponibles

GET /regions
Descripción: devuelve todas las regiones disponibles
 Response 200: lista de regiones
 Response 404: no hay regiones disponibles

POST /calculate
Descripción: calcula CO₂ y equivalencias. Indica tokens_input y tokens_output, o bien task_type
 (simple | medium | complex) para usar el presupuesto documentado. Los tokens explícitos tienen prioridad.
 Request:
{
 "tokens_input": 1000,
 "tokens_output": 2000,
 "model_id": 1,
 "region": "España"
}
 o bien
{
 "task_type": "medium",
 "model_id": 1,
 "region": "España"
}
Response 200:
{
 "calculation": {"tokens_total":3000, "kwh":0.0035, "co2_kg":0.0009, "kwh_por_millon_tokens":1.165, "intensidad_carbono_kg_kwh":0.258},
 "equivalences": {"car_km":0.015,"streaming_hours":0.009}
}
Errores posibles:
400 → tokens negativos


404 → modelo o región no encontrados


500 → error interno de cálculo



POST /compare
Descripción: compara dos escenarios
 Request:
{
 "scenario1":{"tokens_input":1000,"tokens_output":2000,"model_id":1,"region":"España"},
 "scenario2":{"tokens_input":1500,"tokens_output":2500,"model_id":2,"region":"España"}
}
Response 200: incluye scenario1, scenario2 y difference

POST /simulate
Descripción: simula CO₂ de curso completo
 Request:
{
 "num_students": 10,
 "activities":[{"name":"Actividad 1","model_id":1,"tokens_per_student":500,"frequency":"weekly","weeks":6}],
 "region":"España"
}
Response 200: incluye total_co2_kg, per_student_co2_kg, equivalences y breakdown_by_activity
 Errores posibles:
400 → num_students <= 0 o tokens negativos


404 → modelo o región no encontrados
