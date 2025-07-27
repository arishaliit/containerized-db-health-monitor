-- This SQL script will be executed automatically when the PostgreSQL container starts for the first time.
-- It creates a simple table and inserts some dummy data for monitoring.
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    log_level VARCHAR(20) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Insert some dummy data
INSERT INTO users (username, email) VALUES
('alice', 'alice@example.com'),
('bob', 'bob@example.com'),
('charlie', 'charlie@example.com')
ON CONFLICT (username) DO NOTHING; -- Avoid inserting duplicates on restart

INSERT INTO logs (message, log_level) VALUES
('Application started successfully', 'INFO'),
('User login attempt', 'DEBUG'),
('Database connection established', 'INFO')
ON CONFLICT DO NOTHING; -- Simple conflict handling for logs, adjust as needed
