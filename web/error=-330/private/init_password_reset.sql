-- ./private/init_password_reset.sql

CREATE DATABASE IF NOT EXISTS password_reset;
USE password_reset;

-- enhanced users table
CREATE TABLE IF NOT EXISTS users (
    username            VARCHAR(50)   NOT NULL UNIQUE,
    password            VARCHAR(70)   NOT NULL,
    email               VARCHAR(100)  PRIMARY KEY,
    reset_token         VARCHAR(32),
    reset_token_expiry  DATETIME,
    is_admin            BOOLEAN       DEFAULT FALSE,
    failed_attempts     INT           DEFAULT 0,
    last_failed_attempt DATETIME
);

-- sample data
INSERT INTO users (username, password, email, is_admin) VALUES
  ('admin', 'S0_5tR1ng5_4r3_m0r3_tHaN_qu3r13s_1n_th3_3nd}', 'admin@sqli-challenge.com', TRUE),
  ('user1', 'password123',      'user1@example.com', FALSE),
  ('user2', 'qwerty',            'user2@example.com', FALSE),
  ('user3', 'alabalaportocala',  'user3@example.com', TRUE);

-- ─── Grant read‐only on password_reset to that same user ───
GRANT SELECT ON password_reset.* TO 'search_user'@'%';
FLUSH PRIVILEGES;
