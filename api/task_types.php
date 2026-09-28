<?php
// GET /api/task_types — presupuestos de tokens por tipo de tarea
require_once __DIR__ . '/../includes/database.php';

require_method('GET');
try {
    json_response(get_all_task_types());
} catch (Throwable $e) {
    error_log("carbon_calculator task_types: " . $e->getMessage());
    api_error(500, "Error al obtener tipos de tarea");
}
