<?php
// POST /api/compare — compara dos escenarios
require_once __DIR__ . '/../includes/calculations.php';

require_method('POST');
$req = read_json_body();

$results = [];
foreach (['scenario1', 'scenario2'] as $key) {
    $sc = $req[$key] ?? null;
    if (!is_array($sc)) {
        api_error(422, "Falta el objeto '$key'");
    }
    $where = " en $key";
    $model_id = int_field($sc, 'model_id', true, $where);
    $region   = str_field($sc, 'region', true, $where);
    [$t_in, $t_out] = resolve_tokens(
        int_field($sc, 'tokens_input', false, $where),
        int_field($sc, 'tokens_output', false, $where),
        str_field($sc, 'task_type', false, $where),
        $where
    );
    if (!get_model_by_id($model_id)) {
        api_error(404, "Modelo id $model_id no encontrado en $key");
    }
    if (get_region_factor($region) === null) {
        api_error(404, "Región '$region' no encontrada en $key");
    }

    $result = calculate_co2($t_in, $t_out, $model_id, $region);
    $result['equivalences'] = get_equivalences($result['co2_kg']);
    $results[$key] = $result;
}

$c1 = $results['scenario1']['co2_kg'];
$c2 = $results['scenario2']['co2_kg'];
$co2_diff = $c1 - $c2;
$max_co2 = max($c1, $c2);
$co2_diff_pct = $max_co2 != 0 ? abs($co2_diff) / $max_co2 * 100 : 0;
$results['difference'] = [
    'co2_kg'     => py_round($co2_diff, 6),
    'percentage' => py_round($co2_diff_pct, 2),
];

json_response($results);
