<?php
// GET /api/models — lista de modelos IA con coeficiente, fuente y fecha
require_once __DIR__ . '/../includes/database.php';

require_method('GET');
try {
    $models = get_all_models();
} catch (Throwable $e) {
    error_log("carbon_calculator models: " . $e->getMessage());
    api_error(500, "Error al obtener modelos");
}
if (!$models) api_error(404, "No hay modelos disponibles");
json_response($models);
