<?php
/**
 * calculations.php — Lógica de cálculo de la huella de carbono.
 * Port PHP de backend/calculations.py: mismos cálculos y redondeos que la API
 * FastAPI original y que scripts/case_study.py.
 *
 *     CO2 (kg) = N_tokens × (E_Mtoken / 1e6) × CI_grid
 */

require_once __DIR__ . '/database.php';

/**
 * Equivalente a round() de Python: redondeo correcto sobre el valor binario exacto
 * (round() de PHP 8.3 pre-redondea y difiere en algunos casos, p. ej. 1.0586695).
 */
function py_round(float $x, int $digits): float
{
    return (float)sprintf('%.' . $digits . 'F', $x);
}

// =====================================================
// 1. PRESUPUESTO DE TOKENS POR TIPO DE TAREA
// =====================================================
function tokens_for_task(string $task_type): array
{
    $t = get_task_type($task_type);
    if (!$t) {
        throw new DomainException("Tipo de tarea no encontrado: $task_type");
    }
    return [(int)$t['tokens_entrada'], (int)$t['tokens_salida']];
}

/** Si no se indican tokens, usa el presupuesto documentado del tipo de tarea. */
function resolve_tokens(?int $tokens_input, ?int $tokens_output, ?string $task_type, string $where = ''): array
{
    if ($tokens_input === null || $tokens_output === null) {
        if (!$task_type) {
            api_error(400, "Indica tokens_input y tokens_output, o bien task_type$where");
        }
        try {
            [$t_in, $t_out] = tokens_for_task($task_type);
        } catch (DomainException $e) {
            api_error(404, $e->getMessage());
        }
        $tokens_input  ??= $t_in;
        $tokens_output ??= $t_out;
    }
    if ($tokens_input < 0 || $tokens_output < 0) {
        api_error(400, "Tokens no pueden ser negativos$where");
    }
    if ($tokens_input > CC_MAX_TOKENS || $tokens_output > CC_MAX_TOKENS) {
        api_error(400, 'Tokens fuera de rango (máx. ' . CC_MAX_TOKENS . ")$where");
    }
    return [$tokens_input, $tokens_output];
}

// =====================================================
// 2. CÁLCULO PRINCIPAL DE CO2
// =====================================================
function calculate_co2(int $tokens_input, int $tokens_output, int $model_id, string $region): array
{
    if ($tokens_input < 0 || $tokens_output < 0) {
        throw new DomainException('Los tokens no pueden ser negativos');
    }
    $model = get_model_by_id($model_id);
    if (!$model) {
        throw new DomainException('Modelo no encontrado');
    }
    $factor_region = get_region_factor($region);
    if ($factor_region === null) {
        throw new DomainException('Region no encontrada');
    }

    $tokens_total = $tokens_input + $tokens_output;
    $e_mtoken = (float)$model['kwh_por_millon_tokens'];

    // E_Mtoken está en kWh por millón de tokens -> normalizar a kWh/token
    $kwh = $tokens_total * ($e_mtoken / 1000000);
    $co2_kg = $kwh * $factor_region;

    return [
        'co2_kg'                    => py_round($co2_kg, 6),
        'kwh'                       => py_round($kwh, 6),
        'tokens_total'              => $tokens_total,
        'kwh_por_millon_tokens'     => $e_mtoken,
        'intensidad_carbono_kg_kwh' => $factor_region,
    ];
}

// =====================================================
// 3. EQUIVALENCIAS
// =====================================================
function get_equivalences(float $co2_kg): array
{
    if ($co2_kg < 0) {
        throw new DomainException('El CO2 no puede ser negativo');
    }
    $out = [];
    foreach (get_all_equivalences() as $eq) {
        $out[$eq['tipo']] = py_round($co2_kg * (float)$eq['factor_conversion'], 4);
    }
    return $out;
}
