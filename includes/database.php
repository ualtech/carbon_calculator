<?php
/**
 * database.php — Acceso a la BD SQLite y utilidades HTTP/JSON de la API.
 * Port PHP de backend/database.py (Carbon Calculator v2.0.0).
 */

if (!defined('CC_DB_PATH')) {
    define('CC_DB_PATH', dirname(__DIR__) . '/carbon_calculator.db');
}

// Límites de entrada (la API es pública)
const CC_MAX_TOKENS     = 100000000;   // por consulta / por alumno y actividad
const CC_MAX_STUDENTS   = 100000;
const CC_MAX_WEEKS      = 520;
const CC_MAX_ACTIVITIES = 50;

function get_connection(): PDO
{
    static $pdo = null;
    if ($pdo === null) {
        $pdo = new PDO('sqlite:' . CC_DB_PATH);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
        // Sin fichero -journal: www-data solo necesita escribir en el .db, no en el directorio
        $pdo->exec('PRAGMA journal_mode = MEMORY');
    }
    return $pdo;
}

function fetch_all(string $sql, array $params = []): array
{
    $st = get_connection()->prepare($sql);
    $st->execute($params);
    return $st->fetchAll();
}

function fetch_one(string $sql, array $params = []): ?array
{
    $st = get_connection()->prepare($sql);
    $st->execute($params);
    $row = $st->fetch();
    return $row === false ? null : $row;
}

// ===========================
// MODELOS
// ===========================
function get_all_models(): array
{
    return fetch_all('SELECT * FROM modelos ORDER BY id_modelo');
}

function get_model_by_id(int $model_id): ?array
{
    return fetch_one('SELECT * FROM modelos WHERE id_modelo = ?', [$model_id]);
}

// ===========================
// REGIONES
// ===========================
function get_region_factor(string $region_name): ?float
{
    $row = fetch_one('SELECT intensidad_carbono_kg_kwh FROM factores_region WHERE nombre_region = ?', [$region_name]);
    return $row ? (float)$row['intensidad_carbono_kg_kwh'] : null;
}

function get_region_id(string $region_name): ?int
{
    $row = fetch_one('SELECT id_region FROM factores_region WHERE nombre_region = ?', [$region_name]);
    return $row ? (int)$row['id_region'] : null;
}

function get_all_regions(): array
{
    return fetch_all('SELECT * FROM factores_region ORDER BY id_region');
}

// ===========================
// EQUIVALENCIAS
// ===========================
function get_all_equivalences(): array
{
    return fetch_all('SELECT * FROM equivalencias ORDER BY id_equivalencia');
}

// ===========================
// TIPOS DE TAREA (presupuestos de tokens)
// ===========================
function get_all_task_types(): array
{
    return fetch_all('SELECT * FROM tipos_tarea ORDER BY id_tipo');
}

function get_task_type(string $task_type): ?array
{
    return fetch_one('SELECT * FROM tipos_tarea WHERE tipo = ?', [strtolower($task_type)]);
}

// ===========================
// METADATA
// ===========================
function get_metadata(): array
{
    $out = [];
    foreach (fetch_all('SELECT clave, valor FROM metadata') as $r) {
        $out[$r['clave']] = $r['valor'];
    }
    return $out;
}

// ===========================
// LOG DE CONSULTAS (nunca rompe la respuesta)
// ===========================
function log_calculation(array $d): void
{
    try {
        $st = get_connection()->prepare(
            'INSERT INTO consultas_log (fecha_timestamp, id_modelo, id_region, tokens_entrada, tokens_salida, co2_kg)
             VALUES (?, ?, ?, ?, ?, ?)'
        );
        $st->execute([
            date('Y-m-d\TH:i:s'), $d['id_modelo'], $d['id_region'],
            $d['tokens_entrada'], $d['tokens_salida'], $d['co2_kg'],
        ]);
    } catch (Throwable $e) {
        error_log('carbon_calculator: error al loguear cálculo: ' . $e->getMessage());
    }
}

// ===========================
// UTILIDADES HTTP / JSON
// ===========================
function json_response($data, int $status = 200): void
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    header('X-Content-Type-Options: nosniff');
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRESERVE_ZERO_FRACTION);
    exit;
}

/** Error con el mismo formato que FastAPI: {"detail": "..."} */
function api_error(int $status, string $detail): void
{
    json_response(['detail' => $detail], $status);
}

function require_method(string $method): void
{
    if ($_SERVER['REQUEST_METHOD'] !== $method) {
        header('Allow: ' . $method);
        api_error(405, 'Method Not Allowed');
    }
}

function read_json_body(): array
{
    $raw = file_get_contents('php://input', false, null, 0, 65536);
    $data = json_decode($raw ?: '', true);
    if (!is_array($data)) {
        api_error(422, 'El cuerpo de la petición debe ser un objeto JSON válido');
    }
    return $data;
}

/** Entero obligatorio u opcional (acepta 5, 5.0 o "5", como Pydantic). */
function int_field(array $src, string $key, bool $required, string $where = ''): ?int
{
    if (!array_key_exists($key, $src) || $src[$key] === null) {
        if ($required) api_error(422, "Falta el campo '$key'$where");
        return null;
    }
    $v = $src[$key];
    if (is_int($v)) return $v;
    if (is_float($v) && floor($v) == $v && abs($v) < PHP_INT_MAX) return (int)$v;
    if (is_string($v) && preg_match('/^-?\d{1,15}$/', trim($v))) return (int)trim($v);
    api_error(422, "El campo '$key' debe ser un número entero$where");
}

function str_field(array $src, string $key, bool $required, string $where = ''): ?string
{
    if (!array_key_exists($key, $src) || $src[$key] === null) {
        if ($required) api_error(422, "Falta el campo '$key'$where");
        return null;
    }
    if (!is_string($src[$key]) || mb_strlen($src[$key]) > 200) {
        api_error(422, "El campo '$key' debe ser un texto$where");
    }
    return $src[$key];
}
