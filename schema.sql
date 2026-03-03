PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS billing;
DROP TABLE IF EXISTS prescriptions;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS departments;

CREATE TABLE departments (
    department_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT    NOT NULL UNIQUE,
    floor_number    INTEGER NOT NULL,
    capacity        INTEGER NOT NULL CHECK(capacity > 0),
    head_of_dept    TEXT    NOT NULL
);

CREATE TABLE doctors (
    doctor_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name       TEXT    NOT NULL,
    last_name        TEXT    NOT NULL,
    specialisation   TEXT    NOT NULL,
    department_id    INTEGER NOT NULL,
    years_experience INTEGER NOT NULL CHECK(years_experience >= 0),
    email            TEXT    NOT NULL UNIQUE,
    phone            TEXT    NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE patients (
    patient_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name        TEXT    NOT NULL,
    last_name         TEXT    NOT NULL,
    date_of_birth     TEXT    NOT NULL,
    gender            TEXT    NOT NULL CHECK(gender IN ('Male', 'Female', 'Non-Binary', 'Prefer Not to Say')),
    blood_type        TEXT    NOT NULL CHECK(blood_type IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    weight_kg         REAL    NOT NULL CHECK(weight_kg > 0),
    height_cm         REAL    NOT NULL CHECK(height_cm > 0),
    phone             TEXT    NOT NULL,
    address           TEXT    NOT NULL,
    postcode          TEXT    NOT NULL,
    registration_date TEXT    NOT NULL
);

CREATE TABLE appointments (
    appointment_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id        INTEGER NOT NULL,
    doctor_id         INTEGER NOT NULL,
    department_id     INTEGER NOT NULL,
    appointment_date  TEXT    NOT NULL,
    appointment_time  TEXT    NOT NULL,
    triage_priority   TEXT    NOT NULL CHECK(triage_priority IN ('Non-Urgent', 'Standard', 'Urgent', 'Emergency', 'Critical')),
    appointment_status TEXT   NOT NULL CHECK(appointment_status IN ('Scheduled', 'Checked-In', 'In Progress', 'Completed', 'Cancelled')),
    pain_level        INTEGER NOT NULL CHECK(pain_level BETWEEN 0 AND 10),
    notes             TEXT,
    UNIQUE(patient_id, doctor_id, appointment_date, appointment_time),
    FOREIGN KEY (patient_id)    REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id)     REFERENCES doctors(doctor_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE prescriptions (
    prescription_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id    INTEGER NOT NULL,
    patient_id        INTEGER NOT NULL,
    doctor_id         INTEGER NOT NULL,
    medication_name   TEXT    NOT NULL,
    dosage_mg         REAL    NOT NULL CHECK(dosage_mg > 0),
    frequency         TEXT    NOT NULL CHECK(frequency IN ('Once Daily', 'Twice Daily', 'Three Times Daily', 'Four Times Daily', 'As Needed')),
    duration_days     INTEGER NOT NULL CHECK(duration_days > 0),
    prescribed_date   TEXT    NOT NULL,
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id),
    FOREIGN KEY (patient_id)     REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id)      REFERENCES doctors(doctor_id)
);

CREATE TABLE billing (
    billing_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id        INTEGER NOT NULL,
    appointment_id    INTEGER NOT NULL,
    bill_amount       REAL    NOT NULL CHECK(bill_amount >= 0),
    payment_method    TEXT    NOT NULL CHECK(payment_method IN ('Cash', 'Credit Card', 'Debit Card', 'Insurance', 'NHS Funded', 'Bank Transfer')),
    payment_status    TEXT    NOT NULL CHECK(payment_status IN ('Pending', 'Partially Paid', 'Paid', 'Overdue', 'Refunded')),
    billing_date      TEXT    NOT NULL,
    FOREIGN KEY (patient_id)     REFERENCES patients(patient_id),
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id)
);
