<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Delivery extends Model
{
    use HasFactory;

    protected $fillable = [
        'order_id',
        'driver_id',
        'pickup_lat',
        'pickup_lng',
        'dropoff_lat',
        'dropoff_lng',
        'pickup_address',
        'dropoff_address',
        'estimated_time',
        'actual_time',
        'distance_km',
        'status',
        'pickup_time',
        'dropoff_time'
    ];

    protected $casts = [
        'pickup_lat' => 'decimal:8',
        'pickup_lng' => 'decimal:8',
        'dropoff_lat' => 'decimal:8',
        'dropoff_lng' => 'decimal:8',
        'distance_km' => 'decimal:3',
        'estimated_time' => 'integer',
        'actual_time' => 'integer',
        'pickup_time' => 'datetime',
        'dropoff_time' => 'datetime'
    ];

    public function driver()
    {
        return $this->belongsTo(Driver::class);
    }
}
