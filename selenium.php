<?php

header('Content-Type: application/json; charset=utf-8');

set_time_limit(120);

$data = json_decode(file_get_contents('php://input'), true);
$query = $data['query'] ?? '';

$escapedQuery = escapeshellarg($query);
$path = escapeshellarg(__DIR__ . '/main.py');

$command = "python {$path} {$escapedQuery} 2>&1";
$output = shell_exec($command);

echo json_encode([
    'status' => 'success',
    'result' => $output ? trim($output) : '출력 결과가 없거나 에러가 발생했습니다.'
], JSON_UNESCAPED_UNICODE);

?>