-- ============================================================
-- North Eastern Region Landslide Early Warning & Disaster Management Platform
-- Complete Production Database Schema
-- ============================================================

-- 1. Users and RBAC
CREATE TABLE IF NOT EXISTS users (
    id              INT             NOT NULL AUTO_INCREMENT,
    email           VARCHAR(255)    NOT NULL UNIQUE,
    hashed_password VARCHAR(255)    NOT NULL,
    full_name       VARCHAR(255)    NOT NULL,
    phone_number    VARCHAR(32),
    role            ENUM('CITIZEN', 'FIELD_WORKER', 'AUTHORITY', 'ADMIN') NOT NULL DEFAULT 'CITIZEN',
    state           VARCHAR(100),
    district        VARCHAR(100),
    is_active       BOOLEAN         NOT NULL DEFAULT TRUE,
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_users_role (role),
    INDEX idx_users_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Monitored Regional Locations / Stations
CREATE TABLE IF NOT EXISTS locations (
    id              VARCHAR(64)     NOT NULL,
    name            VARCHAR(255)    NOT NULL,
    state           VARCHAR(100)    NOT NULL,
    district        VARCHAR(100),
    latitude        DECIMAL(10, 6)  NOT NULL,
    longitude       DECIMAL(10, 6)  NOT NULL,
    elevation_m     DECIMAL(10, 2)  NOT NULL DEFAULT 500.0,
    slope_degrees   DECIMAL(6, 2)   NOT NULL DEFAULT 15.0,
    population      INT             NOT NULL DEFAULT 5000,
    is_active       BOOLEAN         NOT NULL DEFAULT TRUE,
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_locations_state (state),
    INDEX idx_locations_lat_lng (latitude, longitude)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Live & Historical Alerts
CREATE TABLE IF NOT EXISTS alerts (
    id                  INT             NOT NULL AUTO_INCREMENT,
    location            VARCHAR(255)    NOT NULL,
    state               VARCHAR(100),
    district            VARCHAR(100),
    latitude            DECIMAL(10, 6)  NOT NULL,
    longitude           DECIMAL(10, 6)  NOT NULL,
    risk_level          ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') NOT NULL,
    probability         DECIMAL(5, 4)   NOT NULL,
    status              ENUM('active', 'resolved', 'monitoring') NOT NULL DEFAULT 'active',
    affected_population INT             NOT NULL DEFAULT 0,
    description         TEXT            NOT NULL,
    recommended_action  TEXT,
    escalation_level    VARCHAR(50)     NOT NULL DEFAULT 'LOCAL',
    acknowledged_by     VARCHAR(255),
    acknowledged_at     DATETIME,
    created_at          DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_alerts_status      (status),
    INDEX idx_alerts_risk_level  (risk_level),
    INDEX idx_alerts_state       (state),
    INDEX idx_alerts_created_at  (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Citizen & Field Hazard Reports
CREATE TABLE IF NOT EXISTS hazard_reports (
    id                  VARCHAR(64)     NOT NULL,
    user_id             INT,
    reporter_name       VARCHAR(255),
    contact_info        VARCHAR(255),
    location            VARCHAR(255)    NOT NULL,
    state               VARCHAR(100),
    district            VARCHAR(100),
    latitude            DECIMAL(10, 6)  NOT NULL,
    longitude           DECIMAL(10, 6)  NOT NULL,
    hazard_type         VARCHAR(100)    NOT NULL,
    severity            ENUM('low', 'medium', 'high', 'critical') NOT NULL,
    description         TEXT            NOT NULL,
    visible_cracks      BOOLEAN         NOT NULL DEFAULT FALSE,
    rockfall_observed   BOOLEAN         NOT NULL DEFAULT FALSE,
    road_blocked        BOOLEAN         NOT NULL DEFAULT FALSE,
    water_accumulation  BOOLEAN         NOT NULL DEFAULT FALSE,
    soil_movement       BOOLEAN         NOT NULL DEFAULT FALSE,
    media_url           VARCHAR(512),
    status              ENUM('NEW', 'UNDER_REVIEW', 'VERIFIED', 'ACTION_REQUIRED', 'RESOLVED', 'REJECTED') NOT NULL DEFAULT 'NEW',
    admin_notes         TEXT,
    idempotency_key     VARCHAR(128)    UNIQUE,
    sync_status         VARCHAR(32)     NOT NULL DEFAULT 'SYNCED',
    created_at          DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_reports_status     (status),
    INDEX idx_reports_severity   (severity),
    INDEX idx_reports_state      (state),
    INDEX idx_reports_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Field Report Audit Trail
CREATE TABLE IF NOT EXISTS report_audit_logs (
    id          INT             NOT NULL AUTO_INCREMENT,
    report_id   VARCHAR(64)     NOT NULL,
    changed_by  VARCHAR(255)    NOT NULL,
    old_status  VARCHAR(50)     NOT NULL,
    new_status  VARCHAR(50)     NOT NULL,
    notes       TEXT,
    created_at  DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_audit_report (report_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. ML Predictions History
CREATE TABLE IF NOT EXISTS predictions (
    id              INT             NOT NULL AUTO_INCREMENT,
    prediction_id   VARCHAR(64)     NOT NULL UNIQUE,
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
    soil_moisture   DECIMAL(6, 4),
    explanation     TEXT,
    model_name      VARCHAR(100),
    model_version   VARCHAR(20),
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_pred_risk_level  (risk_level),
    INDEX idx_pred_lat_lng     (latitude, longitude),
    INDEX idx_pred_created_at  (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. Notification Logs (SMS, Push, In-App)
CREATE TABLE IF NOT EXISTS notification_logs (
    id              INT             NOT NULL AUTO_INCREMENT,
    alert_id        INT,
    channel         ENUM('SMS', 'PUSH', 'IN_APP') NOT NULL,
    recipient       VARCHAR(255)    NOT NULL,
    recipient_role  VARCHAR(50),
    message         TEXT            NOT NULL,
    status          ENUM('SENT', 'FAILED', 'DELIVERED', 'QUEUED') NOT NULL DEFAULT 'SENT',
    dedup_hash      VARCHAR(64),
    error_message   TEXT,
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_notif_alert (alert_id),
    INDEX idx_notif_status (status),
    INDEX idx_notif_hash (dedup_hash)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. Push / SMS Subscriptions
CREATE TABLE IF NOT EXISTS notification_subscriptions (
    id              INT             NOT NULL AUTO_INCREMENT,
    user_id         INT,
    phone_number    VARCHAR(32),
    fcm_token       VARCHAR(512),
    endpoint        VARCHAR(512),
    state           VARCHAR(100),
    district        VARCHAR(100),
    min_risk_level  ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') NOT NULL DEFAULT 'HIGH',
    is_active       BOOLEAN         NOT NULL DEFAULT TRUE,
    created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_sub_state (state)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed default administrator account (Password: admin123)
-- Hash generated for: admin123
INSERT IGNORE INTO users (id, email, hashed_password, full_name, phone_number, role, state)
VALUES (1, 'admin@ner-disaster.gov.in', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'NER Disaster Response Authority', '+913642220000', 'ADMIN', 'Meghalaya');

INSERT IGNORE INTO users (id, email, hashed_password, full_name, phone_number, role, state)
VALUES (2, 'officer@sikkim.gov.in', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Sikkim Field Disaster Officer', '+913592200000', 'AUTHORITY', 'Sikkim');
