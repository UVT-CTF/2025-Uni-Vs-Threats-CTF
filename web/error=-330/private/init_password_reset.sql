CREATE DATABASE IF NOT EXISTS password_reset;
USE password_reset;


-- Enhanced users table with reset functionality
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(70) NOT NULL,
    email VARCHAR(100) PRIMARY KEY,
    reset_token VARCHAR(32),
    reset_token_expiry DATETIME,
    is_admin BOOLEAN DEFAULT FALSE,
    failed_attempts INT DEFAULT 0,
    last_failed_attempt DATETIME
);

-- Sample data with enhanced security (but vulnerable setup)
INSERT INTO users (username, password, email, is_admin) VALUES 
('admin', 'S0_5tR1ng5_4r3_m0r3_tHaN_qu3r13s}', 'admin@sqli-challenge.com', TRUE),
('user1', 'password123', 'user1@example.com', FALSE),
('user2', 'qwerty', 'user2@example.com', FALSE),
('user3', 'alabalaportocala', 'user@3example.com', TRUE);

