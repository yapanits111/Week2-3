<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use App\Models\Driver;

class DriverController extends Controller
{
    /**
     * Get all drivers
     */
    public function index(): JsonResponse
    {
        $drivers = Driver::all();
        return response()->json($drivers);
    }

    /**
     * Get specific driver
     */
    public function show($id): JsonResponse
    {
        $driver = Driver::find($id);
        
        if (!$driver) {
            return response()->json(['error' => 'Driver not found'], 404);
        }

        return response()->json($driver);
    }

    /**
     * Create new driver
     */
    public function store(Request $request): JsonResponse
    {
        $request->validate([
            'name' => 'required|string|max:255',
            'email' => 'required|email|unique:drivers',
            'phone' => 'required|string|max:20',
            'license_number' => 'required|string|unique:drivers',
            'vehicle_type' => 'required|string'
        ]);

        $driver = Driver::create($request->all());
        
        return response()->json($driver, 201);
    }

    /**
     * Update driver
     */
    public function update(Request $request, $id): JsonResponse
    {
        $driver = Driver::find($id);
        
        if (!$driver) {
            return response()->json(['error' => 'Driver not found'], 404);
        }

        $request->validate([
            'name' => 'string|max:255',
            'email' => 'email|unique:drivers,email,' . $id,
            'phone' => 'string|max:20',
            'license_number' => 'string|unique:drivers,license_number,' . $id,
            'vehicle_type' => 'string'
        ]);

        $driver->update($request->all());
        
        return response()->json($driver);
    }

    /**
     * Delete driver
     */
    public function destroy($id): JsonResponse
    {
        $driver = Driver::find($id);
        
        if (!$driver) {
            return response()->json(['error' => 'Driver not found'], 404);
        }

        $driver->delete();
        
        return response()->json(['message' => 'Driver deleted successfully']);
    }

    /**
     * Get driver analytics
     */
    public function analytics($id): JsonResponse
    {
        $driver = Driver::find($id);
        
        if (!$driver) {
            return response()->json(['error' => 'Driver not found'], 404);
        }

        // Mock analytics data - in real app, this would come from database
        $analytics = [
            'driver_id' => $driver->id,
            'driver_name' => $driver->name,
            'total_deliveries' => rand(50, 500),
            'avg_delivery_time' => rand(15, 45),
            'completion_rate' => rand(80, 99) / 100,
            'customer_rating' => rand(35, 50) / 10,
            'violations_count' => rand(0, 5),
            'last_drug_test' => 'negative',
            'credential_status' => 'valid',
            'current_status' => rand(0, 1) ? 'available' : 'on_delivery'
        ];

        return response()->json($analytics);
    }
}
