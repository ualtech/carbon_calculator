<?php
// POST /api/simulate — CO2 de un curso completo (alumnos × actividades × semanas)
require_once __DIR__ . '/../includes/calculations.php';

require_method('POST');
$req = read_json_body();

$num_students = int_field($req, 'num_students', true);
$region       = str_field($req, 'region', true);
$activities   = $req['activities'] ?? null;
if (!is_array($activities) || !array_is_list($activities)) {
    api_error(422, "El campo 'activities' debe ser una lista");
}

if ($num_students <= 0) {
    api_error(400, 'Número de estudiantes debe ser mayor que 0');
}
if ($num_students > CC_MAX_STUDENTS) {
    api_error(400, 'Número de estudiantes fuera de rango (máx. ' . CC_MAX_STUDENTS . ')');
}
if (count($activities) > CC_MAX_ACTIVITIES) {
    api_error(400, 'Demasiadas actividades (máx. ' . CC_MAX_ACTIVITIES . ')');
}
if (get_region_factor($region) === null) {
    api_error(404, "Región '$region' no encontrada");
}
$region_id = get_region_id($region);

$total_co2 = 0.0;
$breakdown = [];

foreach ($activities as $i => $act) {
    if (!is_array($act)) {
        api_error(422, 'Actividad ' . ($i + 1) . ' no válida');
    }
    $where = ' en actividad ' . ($i + 1);
    $name     = str_field($act, 'name', true, $where);
    $model_id = int_field($act, 'model_id', true, $where);
    $tokens   = int_field($act, 'tokens_per_student', true, $where);
    $freq     = str_field($act, 'frequency', true, $where);
    $weeks    = int_field($act, 'weeks', true, $where);

    if ($tokens < 0 || $weeks < 1) {
        api_error(400, "Tokens o semanas inválidas en actividad '$name'");
    }
    if ($tokens > CC_MAX_TOKENS || $weeks > CC_MAX_WEEKS) {
        api_error(400, "Tokens o semanas fuera de rango en actividad '$name'");
    }
    if (!get_model_by_id($model_id)) {
        api_error(404, "Modelo id $model_id no encontrado en actividad '$name'");
    }

    switch (strtolower($freq)) {
        case 'daily':   $total_events = $weeks * 7; break;
        case 'weekly':  $total_events = $weeks;     break;
        case 'monthly': $total_events = $weeks / 4; break;
        default:
            api_error(400, "Frecuencia inválida en actividad '$name'. Usa daily, weekly o monthly.");
    }

    $tokens_total = (int)($tokens * $num_students * $total_events);
    $result = calculate_co2($tokens_total, 0, $model_id, $region);
    $total_co2 += $result['co2_kg'];

    $breakdown[] = [
        'activity'     => $name,
        'co2_kg'       => $result['co2_kg'],
        'tokens_total' => $result['tokens_total'],
        'equivalences' => get_equivalences($result['co2_kg']),
    ];

    log_calculation([
        'id_modelo'      => $model_id,
        'id_region'      => $region_id,
        'tokens_entrada' => $tokens * $num_students,
        'tokens_salida'  => 0,
        'co2_kg'         => $result['co2_kg'],
    ]);
}

json_response([
    'total_co2_kg'          => py_round($total_co2, 6),
    'per_student_co2_kg'    => py_round($total_co2 / $num_students, 6),
    'equivalences'          => get_equivalences($total_co2),
    'breakdown_by_activity' => $breakdown,
]);
