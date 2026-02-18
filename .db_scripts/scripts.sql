-- POSTGRESS

CREATE SCHEMA IF NOT EXISTS vg_store;

CREATE TABLE vg_store.role (
    role_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    record_status INT NOT NULL DEFAULT 1
);

INSERT INTO vg_store.role (name) VALUES ('Admin'), ('User'), ('Manager');

CREATE TABLE vg_store.role_permission (
    role_permission_id SERIAL PRIMARY KEY,
    role_id INT REFERENCES vg_store.role(role_id),
    permission VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    record_status INT NOT NULL DEFAULT 1
);

INSERT INTO vg_store.role_permission (role_id, permission) VALUES 
(1, 'Full Access'),
(2, 'Basic Access'),
(3, 'Management Access');


CREATE TABLE vg_store.profile (
    profile_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    record_status INT NOT NULL DEFAULT 1
);

INSERT INTO vg_store.profile (name, description) VALUES 
('Admin Profile', 'Full access to all system features.'),
('User Profile', 'Limited access to basic features.'),
('Manager Profile', 'Access to management features and reports.');

CREATE TABLE vg_store.user_status (
    status_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    record_status INT NOT NULL DEFAULT 1
);

INSERT INTO vg_store.user_status (name, description) VALUES 
('Active', 'User is active and can access the system.'),
('Inactive', 'User is inactive and cannot access the system.'),
('Suspended', 'User is suspended due to policy violations.');

CREATE TABLE vg_store.user (
    user_id SERIAL PRIMARY KEY,
    user_public_key VARCHAR(255) UNIQUE,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    user_status_id INT REFERENCES vg_store.user_status(status_id),
    role_id INT REFERENCES vg_store.role(role_id),
    profile_id INT REFERENCES vg_store.profile(profile_id),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    record_status INT NOT NULL DEFAULT 1
);

/*INSERT INTO vg_store.user (user_public_key, username, password, email, role_id, profile_id) VALUES 
('public_key_1', 'admin_user', 'hashed_password_1', 'admin@example.com', 1, 1),
('public_key_2', 'regular_user', 'hashed_password_2', 'user@example.com', 2, 2);*/

CREATE TABLE vg_store.customer (
    customer_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES vg_store.user(user_id),
    name VARCHAR(100) NOT NULL,
    address TEXT,
    phone VARCHAR(20),
    status INT NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    record_status INT NOT NULL DEFAULT 1
);

-- INSERT INTO vg_store.customer (user_id, name, address, phone) VALUES 
-- (2, 'John Doe', '123 Main St, Anytown, USA', '555-1234'),
-- (2, 'Jane Smith', '456 Elm St, Othertown, USA', '555-5678');


CREATE TABLE vg_store.employee (
    employee_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES vg_store.user(user_id),
    name VARCHAR(100) NOT NULL,
    position VARCHAR(50),
    status INT NOT NULL DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    record_status INT NOT NULL DEFAULT 1
);

-- INSERT INTO vg_store.employee (user_id, name, position) VALUES 
-- (1, 'Alice Johnson', 'System Administrator'),
-- (1, 'Bob Williams', 'Manager');
