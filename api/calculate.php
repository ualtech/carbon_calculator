<?php
// POST /api/calculate — CO2 y equivalencias de una interacción
require_once __DIR__ . '/../includes/calculations.php';

require_method('POST');
$req = read_json_body();

$model_id = int_field($req, 'model_id', true);
$region   = str_field($req, 'region', true);
[$tokens_input, $tokens_output] = resolve_tokens(
    int_field($req, 'tokens_input', false),
    int_field($req, 'tokens_output', false),
    str_field($req, 'task_type', false)
);

if (!get_model_by_id($model_id)) {
    api_error(404, "Modelo con id $model_id no encontrado");
}
if (get_region_factor($region) === null) {
    api_error(404, "Región '$region' no encontrada");
}

try {
    $result = calculate_co2($tokens_input, $tokens_output, $model_id, $region);
    $equivalences = get_equivalences($result['co2_kg']);
} catch (Throwable $e) {
    error_log('carbon_calculator calculate: ' . $e->getMessage());
    api_error(500, 'Error en cálculo o equivalencias');
}

log_calculation([
    'id_modelo'      => $model_id,
    'id_region'      => get_region_id($region),
    'tokens_entrada' => $tokens_input,
    'tokens_salida'  => $tokens_output,
    'co2_kg'         => $result['co2_kg'],
]);

json_response(['calculation' => $result, 'equivalences' => $equivalences]);
