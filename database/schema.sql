-- ================================
-- TABLE: weather_data
-- Stores raw + processed weather data
-- ================================

CREATE TABLE IF NOT EXISTS weather_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    city TEXT NOT NULL,
    
    temperature REAL,
    humidity REAL,
    pressure REAL,
    wind_speed REAL,
    weather_condition TEXT,
    
    timestamp TEXT NOT NULL,
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- ================================
-- TABLE: alerts
-- Stores triggered alerts
-- ================================

CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    city TEXT NOT NULL,
    
    alert_type TEXT NOT NULL,        
    alert_value REAL,
    threshold REAL,
    
    message TEXT,
    
    timestamp TEXT NOT NULL,
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- ================================
-- TABLE: pipeline_runs
-- Tracks each pipeline execution
-- ================================

CREATE TABLE IF NOT EXISTS pipeline_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    start_time TEXT,
    end_time TEXT,
    
    status TEXT,                    
    
    total_cities INTEGER,
    success_count INTEGER,
    failure_count INTEGER,
    alert_count INTEGER,
    
    duration REAL,
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- ================================
-- TABLE: errors
-- Logs failures for monitoring/debugging
-- ================================

CREATE TABLE IF NOT EXISTS errors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    module TEXT,
    error_message TEXT,
    
    timestamp TEXT,
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- ================================
-- INDEXES (Performance Optimization)
-- ================================

CREATE INDEX IF NOT EXISTS idx_weather_city
ON weather_data(city);

CREATE INDEX IF NOT EXISTS idx_weather_timestamp
ON weather_data(timestamp);

CREATE INDEX IF NOT EXISTS idx_alerts_city
ON alerts(city);

CREATE INDEX IF NOT EXISTS idx_alerts_timestamp
ON alerts(timestamp);


-- ================================
-- VIEW (for dashboard)
-- Latest weather per city
-- ================================

CREATE VIEW IF NOT EXISTS latest_weather AS
SELECT w1.*
FROM weather_data w1
INNER JOIN (
    SELECT city, MAX(timestamp) AS max_time
    FROM weather_data
    GROUP BY city
) w2
ON w1.city = w2.city AND w1.timestamp = w2.max_time;


-- ================================
-- VIEW (recent alerts)
-- ================================

CREATE VIEW IF NOT EXISTS recent_alerts AS
SELECT *
FROM alerts
ORDER BY timestamp DESC
LIMIT 50;