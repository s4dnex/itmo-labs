CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    name TEXT,
    latitude DECIMAL NOT NULL CHECK (latitude BETWEEN -90 AND 90),
    longitude DECIMAL NOT NULL CHECK (longitude BETWEEN -180 AND 180),
    installation_date DATE NOT NULL,
    
    CONSTRAINT UNIQUE_LOCATION UNIQUE (latitude, longitude)
);

CREATE TABLE telescopes (
    telescope_id SERIAL PRIMARY KEY,
    location_id INT UNIQUE REFERENCES locations(location_id) ON DELETE SET NULL,
    name TEXT,
    status TEXT NOT NULL CHECK (status IN ('ACTIVE', 'REPAIR', 'STOPPED')),
    height DECIMAL NOT NULL CHECK (height > 0)
);

CREATE TABLE shapes (
    shape_name TEXT PRIMARY KEY,
    description TEXT
);

CREATE TABLE components (
    component_id SERIAL PRIMARY KEY,
    telescope_id INT REFERENCES telescopes(telescope_id) ON DELETE CASCADE,
    shape_name TEXT REFERENCES shapes(shape_name) ON DELETE SET NULL,
    name TEXT NOT NULL,
    purpose TEXT
);

CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    position TEXT NOT NULL,
    hire_date DATE NOT NULL
);

CREATE TABLE maintenances (
    maintenance_id SERIAL PRIMARY KEY,
    telescope_id INT REFERENCES telescopes(telescope_id) ON DELETE CASCADE,
    employee_id INT REFERENCES employees(employee_id) ON DELETE SET NULL,
    start_date DATE NOT NULL,
    end_date DATE CHECK (end_date >= start_date),

    CONSTRAINT UNIQUE_MAINTENANCE UNIQUE (telescope_id, employee_id, start_date)
);

CREATE OR REPLACE FUNCTION create_maintenance_on_repair()
    RETURNS TRIGGER AS $$
DECLARE
    free_employee_id INT;
BEGIN
    IF NEW.status = 'REPAIR' THEN
        SELECT employee_id
        INTO free_employee_id
        FROM employees
        WHERE NOT EXISTS (
            SELECT 1
            FROM maintenances
            WHERE (employees.employee_id = maintenances.employee_id)
              AND (maintenances.end_date IS NULL OR maintenances.end_date > CURRENT_DATE)
        )
        LIMIT 1;

        IF free_employee_id IS NOT NULL THEN
            INSERT INTO maintenances (telescope_id, employee_id, start_date, end_date)
            VALUES (NEW.telescope_id,free_employee_id,CURRENT_DATE,NULL);
        ELSE
            RAISE NOTICE 'Нет доступных сотрудников для техобслуживания.';
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_create_maintenance
    AFTER INSERT OR UPDATE ON telescopes
    FOR EACH ROW
EXECUTE FUNCTION create_maintenance_on_repair();

INSERT INTO locations (name, latitude, longitude, installation_date) VALUES ('Some cool place I think', 22, 23, '2021-01-01');
INSERT INTO telescopes (location_id, name, status, height) VALUES (1, 'Thousand-feet', 'ACTIVE', 304.8);
INSERT INTO shapes (shape_name, description) VALUES ('Triangular', 'Looks like a triangle');
INSERT INTO shapes (shape_name, description) VALUES ('Circular', 'Just a circle');
INSERT INTO components (telescope_id, shape_name, name, purpose) VALUES (1, 'Circular', 'Giant cup', 'Amplify signals?');
INSERT INTO components (telescope_id, shape_name, name, purpose) VALUES (1, 'Triangular', 'Antenna unit', 'Catch signals');
INSERT INTO components (telescope_id, shape_name, name, purpose) VALUES (1, NULL, 'Waveguide', 'Guide waves');
INSERT INTO employees (first_name, last_name, position, hire_date) VALUES ('Johnny', 'Silverhand', 'Engineer', '2000-01-01');
INSERT INTO maintenances (telescope_id, employee_id, start_date, end_date) VALUES (1, 1, '2021-01-01', '2021-01-02');

