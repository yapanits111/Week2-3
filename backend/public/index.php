<?php

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

$request_uri = $_SERVER['REQUEST_URI'];
$method = $_SERVER['REQUEST_METHOD'];

// Simple routing
if ($request_uri === '/api/health' && $method === 'GET') {
    echo json_encode([
        'status' => 'healthy',
        'service' => 'logistics-backend',
        'timestamp' => date('c')
    ]);
    exit;
}

if ($request_uri === '/api/eta/predict' && $method === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    
    // Forward to AI service
    $ai_service_url = 'http://ai-service:5000/predict_eta';
    
    $context = stream_context_create([
        'http' => [
            'method' => 'POST',
            'header' => 'Content-Type: application/json',
            'content' => json_encode($input)
        ]
    ]);
    
    $result = file_get_contents($ai_service_url, false, $context);
    
    if ($result !== false) {
        echo $result;
    } else {
        echo json_encode(['error' => 'AI service unavailable']);
    }
    exit;
}

if ($request_uri === '/api/drivers' && $method === 'GET') {
    echo json_encode([
        [
            'id' => 1,
            'name' => 'Juan Dela Cruz',
            'email' => 'juan@example.com',
            'phone' => '+639123456789',
            'vehicle_type' => 'Motorcycle',
            'status' => 'available'
        ],
        [
            'id' => 2,
            'name' => 'Maria Santos',
            'email' => 'maria@example.com',
            'phone' => '+639987654321',
            'vehicle_type' => 'Van',
            'status' => 'on_delivery'
        ]
    ]);
    exit;
}

// Default route
echo json_encode([
    'message' => 'Logistics AI Dashboard Backend API',
    'version' => '1.0.0',
    'endpoints' => [
        'GET /api/health' => 'Health check',
        'POST /api/eta/predict' => 'ETA prediction',
        'GET /api/drivers' => 'List drivers'
    ]
]);
?>
