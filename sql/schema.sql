CREATE DATABASE IF NOT EXISTS healthcare_analytics;
USE healthcare_analytics;

-- Patients
CREATE TABLE patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_code VARCHAR(20) NOT NULL,
    sex ENUM('M','F','O') NULL,
    dob DATE NULL
);

-- Lab technicians
CREATE TABLE technicians (
    tech_id INT AUTO_INCREMENT PRIMARY KEY,
    tech_name VARCHAR(100) NOT NULL
);

-- Test orders (when test was requested)
CREATE TABLE test_orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    ordered_at DATETIME NOT NULL,
    priority ENUM('ROUTINE','STAT') DEFAULT 'ROUTINE',
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);

-- Test results (when test was completed and verified)
CREATE TABLE test_results (
    result_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    test_name VARCHAR(50) NOT NULL,
    result_value DECIMAL(10,2) NOT NULL,
    unit VARCHAR(20),
    reference_low DECIMAL(10,2),
    reference_high DECIMAL(10,2),
    result_time DATETIME NOT NULL,
    tech_id INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES test_orders(order_id),
    FOREIGN KEY (tech_id) REFERENCES technicians(tech_id)
);
