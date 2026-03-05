-- enable foreign key support (off by default in sqlite)
PRAGMA foreign_keys = ON;

-- drop in reverse order to avoid fk issues
DROP TABLE IF EXISTS billing;
DROP TABLE IF EXISTS prescriptions;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS departments;

-- lookup table for hospital departments
CREATE TABLE departments (
    department_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT    NOT NULL UNIQUE,          -- nominal
    floor_number    INTEGER NOT NULL,                 -- ratio (ground floor = 0)
    capacity        INTEGER NOT NULL CHECK(capacity > 0),  -- ratio (bed count)
    head_of_dept    TEXT    NOT NULL                  -- nominal
);

-- each doctor belongs to one department
CREATE TABLE doctors (
    doctor_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name       TEXT    NOT NULL,
    last_name        TEXT    NOT NULL,
    specialisation   TEXT    NOT NULL,                -- nominal
    department_id    INTEGER NOT NULL,
    years_experience INTEGER NOT NULL CHECK(years_experience >= 0),  -- ratio
    email            TEXT    NOT NULL UNIQUE,
    phone            TEXT    NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- main table with all 4 data types, 1500 rows
CREATE TABLE patients (
    patient_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name        TEXT    NOT NULL,
    last_name         TEXT    NOT NULL,
    date_of_birth     TEXT    NOT NULL,               -- interval
    gender            TEXT    NOT NULL CHECK(gender IN ('Male', 'Female', 'Non-Binary', 'Prefer Not to Say')),  -- nominal
    blood_type        TEXT    NOT NULL CHECK(blood_type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),  -- nominal
    weight_kg         REAL    NOT NULL CHECK(weight_kg > 0),   -- ratio
    height_cm         REAL    NOT NULL CHECK(height_cm > 0),   -- ratio
    phone             TEXT    NOT NULL,
    address           TEXT    NOT NULL,
    postcode          TEXT    NOT NULL,
    registration_date TEXT    NOT NULL                -- interval
);

-- links patients to doctors, compound unique prevents double bookings
CREATE TABLE appointments (
    appointment_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id        INTEGER NOT NULL,
    doctor_id         INTEGER NOT NULL,
    department_id     INTEGER NOT NULL,
    appointment_date  TEXT    NOT NULL,               -- interval
    appointment_time  TEXT    NOT NULL,               -- interval
    triage_priority   TEXT    NOT NULL CHECK(triage_priority IN ('Non-Urgent', 'Standard', 'Urgent', 'Emergency', 'Critical')),  -- ordinal
    appointment_status TEXT   NOT NULL CHECK(appointment_status IN ('Scheduled', 'Checked-In', 'In Progress', 'Completed', 'Cancelled')),  -- ordinal
    pain_level        INTEGER NOT NULL CHECK(pain_level BETWEEN 0 AND 10),  -- ordinal (0-10 scale)
    notes             TEXT,
    UNIQUE(patient_id, doctor_id, appointment_date, appointment_time),
    FOREIGN KEY (patient_id)    REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id)     REFERENCES doctors(doctor_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- not every appointment gets a prescription, so separate table
CREATE TABLE prescriptions (
    prescription_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id    INTEGER NOT NULL,
    patient_id        INTEGER NOT NULL,
    doctor_id         INTEGER NOT NULL,
    medication_name   TEXT    NOT NULL,               -- nominal
    dosage_mg         REAL    NOT NULL CHECK(dosage_mg > 0),  -- ratio
    frequency         TEXT    NOT NULL CHECK(frequency IN ('Once Daily', 'Twice Daily', 'Three Times Daily', 'Four Times Daily', 'As Needed')),  -- ordinal
    duration_days     INTEGER NOT NULL CHECK(duration_days > 0),  -- ratio
    prescribed_date   TEXT    NOT NULL,               -- interval
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id),
    FOREIGN KEY (patient_id)     REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id)      REFERENCES doctors(doctor_id)
);

-- billing has its own lifecycle (pending/paid/overdue) so kept separate
CREATE TABLE billing (
    billing_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id        INTEGER NOT NULL,
    appointment_id    INTEGER NOT NULL,
    bill_amount       REAL    NOT NULL CHECK(bill_amount >= 0),  -- ratio
    payment_method    TEXT    NOT NULL CHECK(payment_method IN ('Cash', 'Credit Card', 'Debit Card', 'Insurance', 'NHS Funded', 'Bank Transfer')),  -- nominal
    payment_status    TEXT    NOT NULL CHECK(payment_status IN ('Pending', 'Partially Paid', 'Paid', 'Overdue', 'Refunded')),  -- ordinal
    billing_date      TEXT    NOT NULL,               -- interval
    FOREIGN KEY (patient_id)     REFERENCES patients(patient_id),
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id)
);
