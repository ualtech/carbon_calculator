<?php
// GET /api/version — versión de la herramienta y fecha de la BD
require_once __DIR__ . '/../includes/database.php';

require_method('GET');
json_response(get_metadata());
