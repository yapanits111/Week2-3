-- Week 4: Smart Warehousing & Inventory Management Database Schema

-- Inventory alerts table for stock monitoring
CREATE TABLE IF NOT EXISTS inventory_alerts (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(100) NOT NULL,
    product_name VARCHAR(255),
    stock INT NOT NULL,
    min_threshold INT DEFAULT 20,
    alert TEXT,
    alert_type VARCHAR(50) DEFAULT 'LOW_STOCK',
    zone VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- RFID logs table for tracking product movement
CREATE TABLE IF NOT EXISTS rfid_logs (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(100) NOT NULL,
    rfid_tag VARCHAR(100),
    location VARCHAR(100),
    zone VARCHAR(100),
    action VARCHAR(50) DEFAULT 'SCAN', -- SCAN, MOVE, PICK, PLACE
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    device_id VARCHAR(100),
    employee_id VARCHAR(100)
);

-- Sales data for demand forecasting
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(100) NOT NULL,
    product_name VARCHAR(255),
    quantity_sold INT NOT NULL,
    revenue DECIMAL(10,2),
    month INT NOT NULL,
    year INT NOT NULL,
    week INT,
    day_of_week INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sensor data for environmental monitoring
CREATE TABLE IF NOT EXISTS sensor_data (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(100) NOT NULL,
    sensor_type VARCHAR(50), -- TEMPERATURE, HUMIDITY, MOTION, WEIGHT
    zone VARCHAR(100),
    value DECIMAL(10,2),
    unit VARCHAR(20),
    status VARCHAR(50) DEFAULT 'NORMAL', -- NORMAL, WARNING, CRITICAL
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample warehouse data
INSERT INTO inventory_alerts (product_id, product_name, stock, min_threshold, alert, zone) VALUES
('PROD001', 'Electronics - Smartphone', 15, 20, 'Low stock alert: Only 15 units remaining', 'Zone A'),
('PROD002', 'Clothing - T-Shirt', 45, 30, 'Stock OK', 'Zone B'), 
('PROD003', 'Books - Programming Guide', 8, 15, 'Critical: Only 8 units left', 'Zone C'),
('PROD004', 'Home - Kitchen Appliance', 25, 20, 'Stock OK', 'Zone A'),
('PROD005', 'Sports - Basketball', 12, 25, 'Low stock alert: Only 12 units remaining', 'Zone D'),
('PROD006', 'Tools - Drill Set', 35, 15, 'Stock OK', 'Zone E'),
('PROD007', 'Garden - Plant Fertilizer', 5, 10, 'Critical: Only 5 units left', 'Zone F'),
('PROD008', 'Auto - Car Parts', 28, 20, 'Stock OK', 'Zone G');

INSERT INTO rfid_logs (product_id, rfid_tag, location, zone, action, device_id, employee_id) VALUES
('PROD001', 'RFID001', 'Shelf A1', 'Zone A', 'SCAN', 'READER001', 'EMP001'),
('PROD002', 'RFID002', 'Shelf B2', 'Zone B', 'MOVE', 'READER002', 'EMP002'),
('PROD003', 'RFID003', 'Shelf C1', 'Zone C', 'PICK', 'READER003', 'EMP001'),
('PROD004', 'RFID004', 'Shelf A3', 'Zone A', 'PLACE', 'READER001', 'EMP003'),
('PROD005', 'RFID005', 'Shelf D1', 'Zone D', 'SCAN', 'READER004', 'EMP002'),
('PROD006', 'RFID006', 'Shelf E2', 'Zone E', 'MOVE', 'READER005', 'EMP001'),
('PROD007', 'RFID007', 'Shelf F1', 'Zone F', 'SCAN', 'READER006', 'EMP003'),
('PROD008', 'RFID008', 'Shelf G1', 'Zone G', 'PICK', 'READER007', 'EMP002');

INSERT INTO sales (product_id, product_name, quantity_sold, revenue, month, year, week) VALUES
('PROD001', 'Electronics - Smartphone', 25, 12500.00, 8, 2025, 32),
('PROD002', 'Clothing - T-Shirt', 40, 800.00, 8, 2025, 32),
('PROD003', 'Books - Programming Guide', 15, 450.00, 8, 2025, 32),
('PROD004', 'Home - Kitchen Appliance', 12, 1800.00, 8, 2025, 32),
('PROD005', 'Sports - Basketball', 18, 540.00, 8, 2025, 32),
('PROD006', 'Tools - Drill Set', 8, 800.00, 7, 2025, 31),
('PROD007', 'Garden - Plant Fertilizer', 22, 330.00, 7, 2025, 31),
('PROD008', 'Auto - Car Parts', 14, 2100.00, 7, 2025, 31);

INSERT INTO sensor_data (sensor_id, sensor_type, zone, value, unit, status) VALUES
('TEMP001', 'TEMPERATURE', 'Zone A', 22.5, 'C', 'NORMAL'),
('TEMP002', 'TEMPERATURE', 'Zone B', 28.3, 'C', 'WARNING'),
('HUM001', 'HUMIDITY', 'Zone A', 45.2, '%', 'NORMAL'),
('HUM002', 'HUMIDITY', 'Zone C', 65.8, '%', 'WARNING'),
('MOTION001', 'MOTION', 'Zone D', 1.0, 'boolean', 'NORMAL'),
('WEIGHT001', 'WEIGHT', 'Zone E', 850.5, 'kg', 'NORMAL'),
('WEIGHT002', 'WEIGHT', 'Zone F', 1200.8, 'kg', 'CRITICAL');
