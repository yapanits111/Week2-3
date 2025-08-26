<?php

use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
*/

Route::get('/', function () {
    return response()->json([
        'message' => 'Logistics AI Dashboard Backend API',
        'version' => '1.0.0',
        'endpoints' => [
            'api/health' => 'Health check',
            'api/eta/predict' => 'ETA prediction',
            'api/eta/train-model' => 'Train ML model',
            'api/drivers' => 'Driver management',
        ]
    ]);
});
