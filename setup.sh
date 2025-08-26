#!/bin/bash

# Fullstack AI Dashboard Setup Script
echo "🚀 Setting up Fullstack AI-Driven Delivery Dashboard..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create environment file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating backend environment file..."
    cp backend/.env.example backend/.env 2>/dev/null || echo "Warning: .env.example not found, using existing .env"
fi

# Build and start services
echo "🏗️  Building and starting services..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Install backend dependencies and run migrations
echo "📦 Installing backend dependencies..."
docker-compose exec -T backend composer install --no-dev --optimize-autoloader

echo "🔧 Running database migrations..."
docker-compose exec -T backend php artisan migrate --force

echo "🌱 Seeding database with sample data..."
docker-compose exec -T backend php artisan db:seed --force

# Train the AI model
echo "🤖 Training AI model for ETA prediction..."
curl -X POST http://localhost:5000/train_model -H "Content-Type: application/json" || echo "Warning: Could not train AI model automatically"

echo "🎉 Setup complete!"
echo ""
echo "📱 Access your applications:"
echo "   Frontend Dashboard: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   AI Service: http://localhost:5000"
echo "   Metabase Analytics: http://localhost:3001"
echo ""
echo "🔧 To stop all services: docker-compose down"
echo "🔄 To restart services: docker-compose restart"
echo "📊 To view logs: docker-compose logs [service-name]"
echo ""
echo "📚 Check README.md for detailed usage instructions"
