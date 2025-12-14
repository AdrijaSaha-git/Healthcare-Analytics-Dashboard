USE healthcare_analytics;

-- Patients
INSERT INTO patients (patient_code, sex, dob) VALUES
('P001', 'F', '1990-01-10'),
('P002', 'M', '1985-05-22'),
('P003', 'F', '2000-08-15');

-- Technicians
INSERT INTO technicians (tech_name) VALUES
('Tech A'),
('Tech B');

-- Test orders
INSERT INTO test_orders (patient_id, ordered_at, priority) VALUES
(1, '2025-01-01 08:00:00', 'ROUTINE'),
(2, '2025-01-01 09:00:00', 'ROUTINE'),
(3, '2025-01-02 10:00:00', 'STAT'),
(1, '2025-01-03 08:30:00', 'ROUTINE'),
(2, '2025-01-03 11:15:00', 'STAT');

-- Assume tests: Hb, Glucose, Creatinine
-- Ref ranges: Hb 12–16, Glucose 70–110, Creatinine 0.6–1.3

INSERT INTO test_results
(order_id, test_name, result_value, unit, reference_low, reference_high, result_time, tech_id)
VALUES
-- Day 1
(1, 'Hemoglobin', 13.5, 'g/dL', 12, 16, '2025-01-01 10:00:00', 1),
(1, 'Glucose', 140, 'mg/dL', 70, 110, '2025-01-01 10:05:00', 1), -- abnormal
(2, 'Glucose', 95, 'mg/dL', 70, 110, '2025-01-01 10:30:00', 2),

-- Day 2
(3, 'Creatinine', 1.6, 'mg/dL', 0.6, 1.3, '2025-01-02 11:00:00', 2), -- abnormal
(3, 'Glucose', 105, 'mg/dL', 70, 110, '2025-01-02 11:05:00', 2),

-- Day 3
(4, 'Hemoglobin', 11.0, 'g/dL', 12, 16, '2025-01-03 09:30:00', 1), -- abnormal low
(4, 'Glucose', 100, 'mg/dL', 70, 110, '2025-01-03 09:40:00', 1),
(5, 'Creatinine', 1.0, 'mg/dL', 0.6, 1.3, '2025-01-03 12:00:00', 2);
