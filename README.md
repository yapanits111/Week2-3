# Fullstack AI-Driven Delivery Dashboard with Profiling & Analytics

A comprehensive logistics management system featuring driver profiling, AI-powered ETA prediction, and real-time analytics.

## 🚀 Features

### Week 3: AI-Powered ETA Prediction
- **Machine Learning Model**: Random Forest model for delivery time prediction
- **Real-time Tracking**: GPS-based position tracking and distance calculation
- **Proximity Notifications**: Smart notifications based on delivery proximity
- **Historical Data Analysis**: Learn from past delivery patterns

<img width="1309" height="875" alt="Screenshot 2025-08-26 181244" src="https://github.com/user-attachments/assets/d0ed641b-25e3-49a6-b6ba-2260f7bdaac1" />

### Analytics & Reporting
- **Metabase Integration**: Professional dashboards and reporting
- **Performance Metrics**: Driver performance scoring and analytics
- **Trend Analysis**: Historical data visualization and insights

## 🏗️ Architecture

```
fullstack-ai-dashboard/
├── ai-service/                  # Flask microservice with ML model
│   ├── app.py                  # Main Flask application
│   ├── model.pkl               # Trained ML model
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile
│
├── backend/                    # Laravel API backend
│   ├── app/Models/             # Driver, Violation, Feedback models
│   ├── app/Http/Controllers/   # API controllers
│   ├── database/migrations/    # Database schema
│   ├── routes/api.php          # API routes
│   └── Dockerfile
│
├── frontend/                   # Next.js + TypeScript frontend
│   ├── app/                    # App router pages
│   ├── components/             # Reusable components
│   └── Dockerfile
│
├── metabase/                   # Analytics platform
│   └── docker-compose.yml
│
└── docker-compose.yml          # Main orchestrator
```

## 🛠️ Technology Stack

### Backend
- **Laravel 11**: PHP framework for API development
- **PostgreSQL**: Primary database for driver and logistics data
- **Redis**: Caching and background job processing

### AI Service
- **Flask**: Python web framework
- **Scikit-learn**: Machine learning library
- **Pandas/NumPy**: Data processing
- **Geopy**: Geographic calculations

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Radix UI**: Accessible component library

### Analytics
- **Metabase**: Business intelligence and dashboards
- **PostgreSQL**: Data warehouse for analytics

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

## 📦 Installation & Setup

### Prerequisites
- Docker and Docker Compose installed
- Git for version control

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fullstack-ai-dashboard
   ```

2. **Environment Setup**
   ```bash
   # Copy environment file for Laravel backend
   cp backend/.env.example backend/.env
   
   # Update database credentials in backend/.env
   DB_CONNECTION=pgsql
   DB_HOST=postgres
   DB_PORT=5432
   DB_DATABASE=logistics_db
   DB_USERNAME=postgres
   DB_PASSWORD="password"
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Initialize the database**
   ```bash
   # Run migrations
   docker-compose exec backend php artisan migrate
   
   # Seed sample data
   docker-compose exec backend php artisan db:seed
   ```

5. **Train the AI model**
   ```bash
   # Train the ETA prediction model
   curl -X POST http://localhost:5000/train_model
   ```

### Service Access

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Main dashboard |
| Backend API | http://localhost:8000 | Laravel API |
| AI Service | http://localhost:5000 | ML prediction service |
| Metabase | http://localhost:3001 | Analytics dashboard |
| PostgreSQL | localhost:5432 | Database |
| Redis | localhost:6379 | Cache/Queue |

## 🎯 Usage Guide

### Driver Management

1. **View All Drivers**: Navigate to `/drivers` to see the driver list
2. **Driver Profile**: Click on any driver to view detailed profile
3. **Performance Tracking**: Monitor drug tests, violations, and feedback
4. **Credential Management**: Track document validity and expiry dates

### ETA Prediction

1. **Get ETA**: Send POST request to `/ai/predict_eta` with coordinates
   ```bash
   curl -X POST http://localhost:5000/predict_eta \
     -H "Content-Type: application/json" \
     -d '{
       "current_lat": 14.5995,
       "current_lng": 120.9842,
       "dropoff_lat": 14.6091,
       "dropoff_lng": 121.0223
     }'
   ```

2. **Response**: Get ETA in minutes and proximity-based message

### Analytics Dashboard

1. **Setup Metabase**: First-time setup at http://localhost:3001
2. **Connect Database**: Use PostgreSQL connection details
3. **Create Dashboards**: Build custom analytics dashboards

## 🔧 API Documentation

### Driver Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/drivers` | List all drivers |
| POST | `/api/drivers` | Create new driver |
| GET | `/api/drivers/{id}` | Get driver details |
| GET | `/api/drivers/{id}/profile` | Get driver profile with analytics |
| PUT | `/api/drivers/{id}` | Update driver |
| DELETE | `/api/drivers/{id}` | Delete driver |

### AI Service Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/train_model` | Train ETA prediction model |
| POST | `/predict_eta` | Predict delivery ETA |
| POST | `/driver_analytics` | Get driver performance analytics |

## 📊 Database Schema

### Core Tables
- `drivers`: Driver personal information
- `drug_test_results`: Drug testing history
- `violations`: Traffic violations and fines
- `feedback`: Customer feedback and ratings
- `credentials`: Driver licenses and certifications
- `infractions`: Work-related incidents

### Relationships
- One driver has many: drug tests, violations, feedback, credentials, infractions
- Comprehensive foreign key constraints for data integrity

## 🚀 Development

### Local Development Setup

1. **Backend Development**
   ```bash
   cd backend
   composer install
   php artisan serve --host=0.0.0.0 --port=8000
   ```

2. **Frontend Development**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **AI Service Development**
   ```bash
   cd ai-service
   pip install -r requirements.txt
   python app.py
   ```

### Adding New Features

1. **Database Changes**: Create migrations in `backend/database/migrations/`
2. **API Endpoints**: Add controllers in `backend/app/Http/Controllers/`
3. **Frontend Pages**: Create components in `frontend/app/`
4. **AI Features**: Extend `ai-service/app.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is open-source and available under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL container is running
   - Check database credentials in `.env`

2. **Frontend Build Errors**
   - Run `npm install` to ensure dependencies are installed
   - Check Node.js version compatibility

3. **AI Model Training Fails**
   - Verify Python dependencies are installed
   - Check Redis connection for caching

4. **Docker Issues**
   - Run `docker-compose down && docker-compose up -d` to restart
   - Check Docker logs: `docker-compose logs [service-name]`

### Support

For technical support, please create an issue in the repository with:
- Detailed error description
- Steps to reproduce
- System information
- Docker logs if applicable

---
