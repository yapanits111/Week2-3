<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ETAController;
use App\Http\Controllers\DriverController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
*/

Route::middleware('api')->group(function () {
    
    // ETA Prediction Routes
    Route::prefix('eta')->group(function () {
        Route::post('/predict', [ETAController::class, 'predictETA']);
        Route::post('/train-model', [ETAController::class, 'trainModel']);
        Route::get('/health', [ETAController::class, 'healthCheck']);
    });

    // Driver Management Routes
    Route::apiResource('drivers', DriverController::class);
    Route::get('drivers/{id}/analytics', [DriverController::class, 'analytics']);

    // Health check
    Route::get('/health', function () {
        return response()->json([
            'status' => 'healthy',
            'service' => 'logistics-backend',
            'timestamp' => now()->toISOString()
        ]);
    });
});
