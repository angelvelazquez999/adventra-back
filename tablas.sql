-- =======================================
-- ADVENTRA — BASE DE DATOS
-- =======================================

-- Habilitar UUID (solo se usa UUID generado desde la app)
-- En MySQL se recomienda pasar UUID desde backend

-- =========================
-- USERS
-- =========================
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role ENUM('company', 'transporter', 'admin') NOT NULL,
    phone VARCHAR(20),
    status ENUM('active', 'disabled') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- COMPANIES
-- =========================
CREATE TABLE companies (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    legal_name VARCHAR(255) NOT NULL,
    rfc VARCHAR(20) NOT NULL,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_company_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- =========================
-- TRANSPORTERS
-- =========================
CREATE TABLE transporters (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    rating DECIMAL(3,2) DEFAULT 0,
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_transporter_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- =========================
-- DOCUMENTS
-- =========================
CREATE TABLE documents (
    id CHAR(36) PRIMARY KEY,
    transporter_id CHAR(36) NOT NULL,
    type VARCHAR(50) NOT NULL, -- license / insurance / permit / rfc
    url TEXT NOT NULL,
    expiry_date DATE,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_document_transporter FOREIGN KEY (transporter_id) REFERENCES transporters(id) ON DELETE CASCADE
);

-- =========================
-- VEHICLES
-- =========================
CREATE TABLE vehicles (
    id CHAR(36) PRIMARY KEY,
    transporter_id CHAR(36) NOT NULL,
    type VARCHAR(100) NOT NULL,   -- pickup / 3.5t / trailer / etc.
    plate VARCHAR(20) UNIQUE NOT NULL,
    capacity_kg INT,
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_vehicle_transporter FOREIGN KEY (transporter_id) REFERENCES transporters(id) ON DELETE CASCADE
);

-- =========================
-- TRIPS
-- =========================
CREATE TABLE trips (
    id CHAR(36) PRIMARY KEY,
    company_id CHAR(36) NOT NULL,
    transporter_id CHAR(36),
    vehicle_id CHAR(36),
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    load_type VARCHAR(150),
    weight DECIMAL(10,2),
    status ENUM('requested', 'assigned', 'in_route', 'completed', 'cancelled') DEFAULT 'requested',
    price DECIMAL(10,2),
    assigned_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_trip_company FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    CONSTRAINT fk_trip_transporter FOREIGN KEY (transporter_id) REFERENCES transporters(id),
    CONSTRAINT fk_trip_vehicle FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
);

-- =========================
-- TRIP EVENTS (GPS / fotos / etc.)
-- =========================
CREATE TABLE trip_events (
    id CHAR(36) PRIMARY KEY,
    trip_id CHAR(36) NOT NULL,
    type VARCHAR(50) NOT NULL,   -- gps_update / pickup_photo / delivery_photo
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_trip_event_trip FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
);

-- =========================
-- PAYMENTS
-- =========================
CREATE TABLE payments (
    id CHAR(36) PRIMARY KEY,
    trip_id CHAR(36) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'paid', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_payment_trip FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
);

-- =========================
-- REVIEWS
-- =========================
CREATE TABLE reviews (
    id CHAR(36) PRIMARY KEY,
    trip_id CHAR(36) NOT NULL,
    user_id CHAR(36) NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_review_trip FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
    CONSTRAINT fk_review_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
