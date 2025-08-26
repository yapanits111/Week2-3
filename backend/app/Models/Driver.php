<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class Driver extends Model
{
    use HasFactory, SoftDeletes;

    protected $fillable = [
        'name',
        'email',
        'phone',
        'license_number',
        'vehicle_type',
        'status',
        'current_lat',
        'current_lng'
    ];

    protected $casts = [
        'current_lat' => 'decimal:8',
        'current_lng' => 'decimal:8',
        'created_at' => 'datetime',
        'updated_at' => 'datetime'
    ];

    public function deliveries()
    {
        return $this->hasMany(Delivery::class);
    }
}
