<?php
// GET /api/ — estado de la API
require_once __DIR__ . '/../includes/database.php';

require_method('GET');
$meta = get_metadata();
json_response(["message" => "Carbon Calculator API running", "version" => $meta["tool_version"] ?? null]);
