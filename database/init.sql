-- Network Auditor Database Initialization Script
-- Author: Golub Daniil Nikolaevich

CREATE DATABASE network_auditor;

-- Table 1: User roles
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    permissions JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: Users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id INTEGER REFERENCES roles(id),
    full_name VARCHAR(100),
    email VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Table 3: Network segments
CREATE TABLE network_segments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    ip_range VARCHAR(50),
    segment_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 4: Network assets
CREATE TABLE assets (
    id SERIAL PRIMARY KEY,
    segment_id INTEGER REFERENCES network_segments(id),
    ip_address VARCHAR(15) NOT NULL,
    hostname VARCHAR(100),
    os_type VARCHAR(50),
    asset_type VARCHAR(50),
    is_critical BOOLEAN DEFAULT FALSE,
    last_scan TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 5: Vulnerability database
CREATE TABLE vulnerability_db (
    id SERIAL PRIMARY KEY,
    port INTEGER NOT NULL,
    service VARCHAR(50),
    risk_level VARCHAR(20),
    description TEXT,
    cve_id VARCHAR(20),
    recommendation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 6: Scan tasks
CREATE TABLE scan_tasks (
    id SERIAL PRIMARY KEY,
    segment_id INTEGER REFERENCES network_segments(id),
    created_by INTEGER REFERENCES users(id),
    ip_range VARCHAR(50) NOT NULL,
    ports_list TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 7: Scan results
CREATE TABLE scan_results (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES scan_tasks(id),
    asset_id INTEGER REFERENCES assets(id),
    ip_address VARCHAR(15) NOT NULL,
    port INTEGER NOT NULL,
    is_open BOOLEAN DEFAULT FALSE,
    service_name VARCHAR(50),
    vulnerability_id INTEGER REFERENCES vulnerability_db(id),
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 8: Reports
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    generated_by INTEGER REFERENCES users(id),
    report_type VARCHAR(50),
    file_path VARCHAR(255),
    report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

-- Table 9: Audit logs
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    details TEXT,
    ip_address VARCHAR(15),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 10: System settings
CREATE TABLE system_settings (
    id SERIAL PRIMARY KEY,
    param_name VARCHAR(100) UNIQUE NOT NULL,
    param_value TEXT,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);