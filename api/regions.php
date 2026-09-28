<?php
// GET /api/regions — regiones con intensidad de carbono
require_once __DIR__ . '/../includes/database.php';

require_method('GET');
try {
    $regions = get_all_regions();
} catch (Throwable $e) {
    error_log("carbon_calculator regions: " . $e->getMessage());
    api_error(500, "Error al obtener regiones");
}
if (!$regions) api_error(404, "No hay regiones disponibles");
json_response($regions);
