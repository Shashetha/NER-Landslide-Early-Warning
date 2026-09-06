-- ============================================================
-- Landslide Early Warning System — MySQL Schema
-- ============================================================

CREATE TABLE IF NOT EXISTS alerts (
    id              INT             NOT NULL AUTO_INCREMENT,
    location        VARCHAR(255)    NOT NULL,
    latitude        DECIMAL(10, 6)  NOT NULL,
    longitude       DECIMAL(10, 6)  NOT NULL,
    risk_level      ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') NOT NULL,
    probability     DECIMAL(5, 4)   NOT NULL,
    status          ENUM('active', 'resolved', 'monitoring') NOT NULL DEFAULT 'active',
    affected_population INT         NOT NULL DEFAULT 0,
    description     TEXT            NOT NULL,
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_alerts_status      (status),
    INDEX idx_alerts_risk_level  (risk_level),
    INDEX idx_alerts_created_at  (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS hazard_reports (
    id              VARCHAR(32)     NOT NULL,
    location        VARCHAR(255)    NOT NULL,
    latitude        DECIMAL(10, 6)  NOT NULL,
    longitude       DECIMAL(10, 6)  NOT NULL,
    hazard_type     VARCHAR(100)    NOT NULL,
    severity        ENUM('low', 'medium', 'high') NOT NULL,
    description     TEXT            NOT NULL,
    contact_info    VARCHAR(255),
    status          ENUM('pending', 'investigating', 'resolved') NOT NULL DEFAULT 'pending',
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_reports_status     (status),
    INDEX idx_reports_severity   (severity),
    INDEX idx_reports_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS predictions (
    id              INT             NOT NULL AUTO_INCREMENT,
    prediction_id   VARCHAR(32)     NOT NULL UNIQUE,
    latitude        DECIMAL(10, 6)  NOT NULL,
    longitude       DECIMAL(10, 6)  NOT NULL,
    risk_level      ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') NOT NULL,
    probability     DECIMAL(5, 4)   NOT NULL,
    confidence      DECIMAL(5, 4)   NOT NULL,
    rainfall_1d     DECIMAL(8, 2),
    rainfall_3d     DECIMAL(8, 2),
    rainfall_7d     DECIMAL(8, 2),
    elevation_m     DECIMAL(10, 2),
    slope_degrees   DECIMAL(6, 2),
    soil_moisture   DECIMAL(6, 2),
    explanation     TEXT,
    model_name      VARCHAR(100),
    model_version   VARCHAR(20),
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_pred_risk_level  (risk_level),
    INDEX idx_pred_lat_lng     (latitude, longitude),
    INDEX idx_pred_created_at  (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- Seed initial alert data
-- ============================================================

INSERT IGNORE INTO alerts
    (id, location, latitude, longitude, risk_level, probability, status, affected_population, description, created_at, updated_at)
VALUES
    (1, 'Gangtok, Sikkim',          27.338900, 88.606500, 'HIGH',     0.8700, 'active',   2500, 'Heavy rainfall detected in the area with steep slope conditions.',                                              DATE_SUB(NOW(), INTERVAL 2 HOUR),  DATE_SUB(NOW(), INTERVAL 12 MINUTE)),
    (2, 'Cherrapunji, Meghalaya',   25.263000, 91.732400, 'CRITICAL', 0.9400, 'active',   5200, 'Critical conditions detected. Multiple risk factors present in wettest place on Earth.',                        DATE_SUB(NOW(), INTERVAL 4 HOUR),  DATE_SUB(NOW(), INTERVAL 30 MINUTE)),
    (3, 'Itanagar, Arunachal Pradesh', 27.084400, 93.605300, 'HIGH',  0.7900, 'active',   1800, 'Elevated soil moisture levels detected in hilly terrain.',                                                      DATE_SUB(NOW(), INTERVAL 6 HOUR),  DATE_SUB(NOW(), INTERVAL 45 MINUTE)),
    (4, 'Shillong, Meghalaya',      25.578800, 91.893300, 'MEDIUM',   0.6200, 'resolved', 3100, 'Risk levels have decreased. Situation stabilized.',                                                             DATE_SUB(NOW(), INTERVAL 48 HOUR), DATE_SUB(NOW(), INTERVAL 12 HOUR)),
    (5, 'Imphal, Manipur',          24.817400, 93.944200, 'HIGH',     0.8100, 'active',   4200, 'Prolonged rainfall over 72 hours causing soil saturation on hill slopes surrounding the valley.',               DATE_SUB(NOW(), INTERVAL 10 HOUR), DATE_SUB(NOW(), INTERVAL 1 HOUR)),
    (6, 'Dimapur, Nagaland',        25.909600, 93.727200, 'MEDIUM',   0.5800, 'monitoring', 1900, 'Moderate risk observed. Soil moisture rising; monitoring continues.',                                         DATE_SUB(NOW(), INTERVAL 20 HOUR), DATE_SUB(NOW(), INTERVAL 3 HOUR)),
    (7, 'Aizawl, Mizoram',          23.727300, 92.717700, 'CRITICAL', 0.9100, 'active',   6100, 'Extreme rainfall event triggering multiple slope failures. Evacuation advisory issued.',                        DATE_SUB(NOW(), INTERVAL 1 HOUR),  DATE_SUB(NOW(), INTERVAL 15 MINUTE)),
    (8, 'Agartala, Tripura',        23.831200, 91.286200, 'LOW',      0.2800, 'resolved', 800,  'Conditions have normalised after brief heavy rainfall episode. No active threat.',                             DATE_SUB(NOW(), INTERVAL 72 HOUR), DATE_SUB(NOW(), INTERVAL 24 HOUR))
