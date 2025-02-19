CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    name TEXT,
    latitude DECIMAL NOT NULL CHECK (latitude BETWEEN -90 AND 90),
    longitude DECIMAL NOT NULL CHECK (longitude BETWEEN -180 AND 180),
    
    CONSTRAINT UNIQUE_LOCATION UNIQUE (latitude, longitude)
);

CREATE TABLE telescopes (
    telescope_id SERIAL PRIMARY KEY,
    location_id INT UNIQUE REFERENCES locations(location_id) ON DELETE SET NULL,
    name TEXT,
    installation_date DATE,
    status TEXT NOT NULL CHECK (status IN ('ACTIVE', 'REPAIR', 'STOPPED')),
    height DECIMAL NOT NULL CHECK (height > 0)
);

CREATE TABLE shapes (
    shape_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE components (
    component_id SERIAL PRIMARY KEY,
    telescope_id INT REFERENCES telescopes(telescope_id) ON DELETE CASCADE,
    shape_id INT REFERENCES shapes(shape_id) ON DELETE SET NULL,
    name TEXT NOT NULL,
    purpose TEXT
);

CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    position TEXT NOT NULL,
    experience INT NOT NULL CHECK (experience >= 0)
);

CREATE TABLE maintenances (
    maintenance_id SERIAL PRIMARY KEY,
    telescope_id INT REFERENCES telescopes(telescope_id) ON DELETE CASCADE,
    employee_id INT REFERENCES employees(employee_id) ON DELETE SET NULL,
    start_date DATE NOT NULL,
    end_date DATE CHECK (end_date >= start_date),

    CONSTRAINT UNIQUE_MAINTENANCE UNIQUE (telescope_id, employee_id, start_date)
);

INSERT INTO locations (name, latitude, longitude) VALUES ('Some cool place I think', 22, 23);

INSERT INTO telescopes (location_id, name, installation_date, status, height) VALUES (1, 'Thousand-feet', '2006-02-24', 'ACTIVE', 304.8);

INSERT INTO shapes (name, description) VALUES ('Triangular', 'Looks like a triangle');
INSERT INTO shapes (name, description) VALUES ('Circular', 'Just a circle');

INSERT INTO components (telescope_id, shape_id, name, purpose) VALUES (1, 2, 'Giant cup', 'Amplify signals?');
INSERT INTO components (telescope_id, shape_id, name, purpose) VALUES (1, 1, 'Antenna unit', 'Catch signals');
INSERT INTO components (telescope_id, shape_id, name, purpose) VALUES (1, NULL, 'Waveguide', 'Guide waves');

INSERT INTO employees (first_name, last_name, position, experience) VALUES ('Johnny', 'Silverhand', 'Engineer', 1);

INSERT INTO maintenances (telescope_id, employee_id, start_date, end_date) VALUES (1, 1, '2021-01-01', '2021-01-02');