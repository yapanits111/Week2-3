<?php

return [
    'name' => env('APP_NAME', 'Logistics Dashboard'),
    'env' => env('APP_ENV', 'production'),
    'debug' => (bool) env('APP_DEBUG', false),
    'url' => env('APP_URL', 'http://localhost:8000'),
    'timezone' => 'UTC',
    'locale' => 'en',
    'key' => env('APP_KEY'),
    'cipher' => 'AES-256-CBC',
    
    'providers' => [
        Illuminate\Foundation\Providers\FoundationServiceProvider::class,
        Illuminate\Database\DatabaseServiceProvider::class,
        Illuminate\Validation\ValidationServiceProvider::class,
        App\Providers\AppServiceProvider::class,
    ],
];
