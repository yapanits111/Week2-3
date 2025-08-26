<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::create('deliveries', function (Blueprint $table) {
            $table->id();
            $table->string('order_id')->unique();
            $table->foreignId('driver_id')->constrained();
            $table->decimal('pickup_lat', 10, 8);
            $table->decimal('pickup_lng', 11, 8);
            $table->decimal('dropoff_lat', 10, 8);
            $table->decimal('dropoff_lng', 11, 8);
            $table->string('pickup_address')->nullable();
            $table->string('dropoff_address')->nullable();
            $table->integer('estimated_time'); // minutes
            $table->integer('actual_time')->nullable(); // minutes
            $table->decimal('distance_km', 8, 3);
            $table->enum('status', ['pending', 'in_progress', 'completed', 'cancelled'])->default('pending');
            $table->timestamp('pickup_time')->nullable();
            $table->timestamp('dropoff_time')->nullable();
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('deliveries');
    }
};
