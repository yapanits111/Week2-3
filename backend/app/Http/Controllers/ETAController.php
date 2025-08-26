<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class ETAController extends Controller
{
    private $aiServiceUrl = 'http://ai-service:5000';

    /**
     * Get ETA prediction from AI service
     */
    public function predictETA(Request $request): JsonResponse
    {
        $request->validate([
            'current_lat' => 'required|numeric|between:-90,90',
            'current_lng' => 'required|numeric|between:-180,180',
            'dropoff_lat' => 'required|numeric|between:-90,90',
            'dropoff_lng' => 'required|numeric|between:-180,180',
        ]);

        try {
            $response = Http::timeout(30)->post($this->aiServiceUrl . '/predict_eta', [
                'current_lat' => $request->current_lat,
                'current_lng' => $request->current_lng,
                'dropoff_lat' => $request->dropoff_lat,
                'dropoff_lng' => $request->dropoff_lng,
            ]);

            if ($response->successful()) {
                return response()->json($response->json());
            }

            return response()->json([
                'error' => 'AI service unavailable'
            ], 503);

        } catch (\Exception $e) {
            Log::error('ETA prediction failed: ' . $e->getMessage());
            
            return response()->json([
                'error' => 'Prediction service temporarily unavailable'
            ], 503);
        }
    }

    /**
     * Train the ML model
     */
    public function trainModel(): JsonResponse
    {
        try {
            $response = Http::timeout(60)->post($this->aiServiceUrl . '/train_model');

            if ($response->successful()) {
                return response()->json($response->json());
            }

            return response()->json([
                'error' => 'Training service unavailable'
            ], 503);

        } catch (\Exception $e) {
            Log::error('Model training failed: ' . $e->getMessage());
            
            return response()->json([
                'error' => 'Training service temporarily unavailable'
            ], 503);
        }
    }

    /**
     * Get AI service health status
     */
    public function healthCheck(): JsonResponse
    {
        try {
            $response = Http::timeout(10)->get($this->aiServiceUrl . '/health');

            if ($response->successful()) {
                return response()->json($response->json());
            }

            return response()->json([
                'status' => 'unhealthy',
                'model_trained' => false
            ]);

        } catch (\Exception $e) {
            return response()->json([
                'status' => 'unavailable',
                'model_trained' => false
            ]);
        }
    }
}
