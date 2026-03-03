import subprocess
import sys

try:
    from faker import Faker
except ImportError:
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])
    from faker import Faker
    print("Packages installed successfully.\n")

import sqlite3
import random

fake = Faker("en_GB")
Faker.seed(42)
random.seed(42)

DB_NAME = "hospital_management.db"
SCHEMA_FILE = "schema.sql"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

with open(SCHEMA_FILE, "r") as f:
    schema_sql = f.read()

conn.executescript(schema_sql)
print(f"Schema loaded from '{SCHEMA_FILE}'")

conn.execute("PRAGMA foreign_keys = ON")

departments_data = [
    ("Emergency Medicine",       0, 50, fake.name()),
    ("Cardiology",               2, 35, fake.name()),
    ("Neurology",                3, 30, fake.name()),
    ("Orthopaedics",             1, 40, fake.name()),
    ("Paediatrics",              4, 45, fake.name()),
    ("Oncology",                 5, 25, fake.name()),
    ("General Surgery",          1, 55, fake.name()),
    ("Dermatology",              3, 20, fake.name()),
    ("Psychiatry",               6, 30, fake.name()),
    ("Obstetrics & Gynaecology", 4, 40, fake.name()),
]

cursor.executemany(
    "INSERT INTO departments (department_name, floor_number, capacity, head_of_dept) VALUES (?, ?, ?, ?)",
    departments_data
)
print(f"Inserted {len(departments_data)} departments.")

specialisations = {
    1:  ["Emergency Medicine", "Trauma Surgery", "Critical Care"],
    2:  ["Interventional Cardiology", "Electrophysiology", "Heart Failure"],
    3:  ["Clinical Neurology", "Neurophysiology", "Stroke Medicine"],
    4:  ["Joint Replacement", "Spinal Surgery", "Sports Medicine"],
    5:  ["Neonatology", "Paediatric Surgery", "Child Psychiatry"],
    6:  ["Medical Oncology", "Radiation Oncology", "Surgical Oncology"],
    7:  ["Colorectal Surgery", "Upper GI Surgery", "Vascular Surgery"],
    8:  ["Clinical Dermatology", "Dermatopathology", "Cosmetic Dermatology"],
    9:  ["General Psychiatry", "Forensic Psychiatry", "Child & Adolescent Psychiatry"],
    10: ["Obstetrics", "Gynaecological Surgery", "Reproductive Medicine"],
}

doctors_data = []
for i in range(50):
    dept_id = (i % 10) + 1
    spec = random.choice(specialisations[dept_id])
    first = fake.first_name()
    last = fake.last_name()
    email = f"{first.lower()}.{last.lower()}{random.randint(1, 999)}@hospital.nhs.uk"
    phone = fake.phone_number()
    years_exp = random.randint(0, 35)
    doctors_data.append((first, last, spec, dept_id, years_exp, email, phone))

cursor.executemany(
    """INSERT INTO doctors (first_name, last_name, specialisation, department_id,
       years_experience, email, phone) VALUES (?, ?, ?, ?, ?, ?, ?)""",
    doctors_data
)
print(f"Inserted {len(doctors_data)} doctors.")

blood_types = ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"]
blood_weights = [35, 13, 30, 8, 8, 2, 2, 2]
genders = ["Male", "Female", "Non-Binary", "Prefer Not to Say"]
gender_weights = [48, 48, 2, 2]

patients_data = []
for _ in range(1500):
    gender = random.choices(genders, weights=gender_weights, k=1)[0]
    if gender == "Male":
        first = fake.first_name_male()
    elif gender == "Female":
        first = fake.first_name_female()
    else:
        first = fake.first_name()
    last = fake.last_name()
    dob = fake.date_of_birth(minimum_age=0, maximum_age=100).strftime("%Y-%m-%d")
    blood = random.choices(blood_types, weights=blood_weights, k=1)[0]
    weight = round(random.gauss(75, 15), 1)
    weight = max(2.5, weight)
    height = round(random.gauss(170, 12), 1)
    height = max(45, height)
    phone = fake.phone_number()
    address = fake.street_address()
    postcode = fake.postcode()
    reg_date = fake.date_between(start_date="-5y", end_date="today").strftime("%Y-%m-%d")
    patients_data.append((first, last, dob, gender, blood, weight, height,
                          phone, address, postcode, reg_date))

cursor.executemany(
    """INSERT INTO patients (first_name, last_name, date_of_birth, gender, blood_type,
       weight_kg, height_cm, phone, address, postcode, registration_date)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
    patients_data
)
print(f"Inserted {len(patients_data)} patients.")

triage_levels = ["Non-Urgent", "Standard", "Urgent", "Emergency", "Critical"]
triage_weights = [25, 35, 20, 15, 5]
statuses = ["Scheduled", "Checked-In", "In Progress", "Completed", "Cancelled"]
status_weights = [10, 5, 5, 70, 10]

notes_templates = [
    "Patient presents with {symptom}. {action} recommended.",
    "Follow-up visit for {condition}. {outcome}.",
    "Routine check-up. All vitals within normal range.",
    "Patient reports {symptom}. Referred to {dept} for further investigation.",
    "Post-operative review. Recovery progressing well.",
    None,
]
symptoms = ["chest pain", "headaches", "joint pain", "skin rash", "fatigue",
            "shortness of breath", "abdominal pain", "dizziness", "back pain",
            "persistent cough"]
actions = ["Further tests", "Medication adjustment", "Physiotherapy",
           "Specialist referral", "Rest and monitoring"]
conditions = ["hypertension", "diabetes", "arthritis", "asthma", "depression",
              "eczema", "migraine", "fracture recovery"]
outcomes = ["Condition stable", "Improvement noted", "Medication increased",
            "Discharged from care", "Further monitoring required"]

appointments_data = []
used_combinations = set()

for _ in range(2000):
    patient_id = random.randint(1, 1500)
    doctor_id = random.randint(1, 50)
    dept_id = ((doctor_id - 1) % 10) + 1
    appt_date = fake.date_between(start_date="-2y", end_date="+1m").strftime("%Y-%m-%d")
    hour = random.randint(8, 17)
    minute = random.choice([0, 30])
    appt_time = f"{hour:02d}:{minute:02d}"

    combo = (patient_id, doctor_id, appt_date, appt_time)
    if combo in used_combinations:
        continue
    used_combinations.add(combo)

    triage = random.choices(triage_levels, weights=triage_weights, k=1)[0]
    status = random.choices(statuses, weights=status_weights, k=1)[0]

    triage_index = triage_levels.index(triage)
    base_pain = triage_index * 2
    pain = min(10, max(0, base_pain + random.randint(-1, 2)))

    note_template = random.choice(notes_templates)
    if note_template:
        notes = note_template.format(
            symptom=random.choice(symptoms),
            action=random.choice(actions),
            condition=random.choice(conditions),
            outcome=random.choice(outcomes),
            dept=random.choice([d[0] for d in departments_data])
        )
    else:
        notes = None

    appointments_data.append((patient_id, doctor_id, dept_id, appt_date,
                              appt_time, triage, status, pain, notes))

cursor.executemany(
    """INSERT INTO appointments (patient_id, doctor_id, department_id,
       appointment_date, appointment_time, triage_priority, appointment_status,
       pain_level, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
    appointments_data
)
print(f"Inserted {len(appointments_data)} appointments.")

medications = {
    "Paracetamol":   {"dosages": [250, 500, 1000], "durations": [3, 5, 7, 14]},
    "Ibuprofen":     {"dosages": [200, 400, 600],  "durations": [5, 7, 10, 14]},
    "Amoxicillin":   {"dosages": [250, 500],        "durations": [5, 7, 10]},
    "Omeprazole":    {"dosages": [10, 20, 40],      "durations": [14, 28, 56]},
    "Metformin":     {"dosages": [500, 850, 1000],  "durations": [30, 60, 90]},
    "Amlodipine":    {"dosages": [5, 10],           "durations": [30, 60, 90]},
    "Sertraline":    {"dosages": [25, 50, 100],     "durations": [30, 60, 90, 180]},
    "Salbutamol":    {"dosages": [100, 200],        "durations": [30, 60]},
    "Codeine":       {"dosages": [15, 30, 60],      "durations": [3, 5, 7]},
    "Prednisolone":  {"dosages": [5, 10, 25],       "durations": [5, 7, 14, 21]},
    "Ciprofloxacin": {"dosages": [250, 500, 750],   "durations": [5, 7, 10, 14]},
    "Diazepam":      {"dosages": [2, 5, 10],        "durations": [3, 5, 7]},
    "Atorvastatin":  {"dosages": [10, 20, 40, 80],  "durations": [30, 60, 90]},
    "Ramipril":      {"dosages": [1.25, 2.5, 5, 10],"durations": [30, 60, 90]},
    "Co-codamol":    {"dosages": [8, 15, 30],       "durations": [3, 5, 7]},
}

frequencies = ["Once Daily", "Twice Daily", "Three Times Daily",
               "Four Times Daily", "As Needed"]
freq_weights = [30, 35, 15, 5, 15]

eligible_appointments = [
    (i + 1, a) for i, a in enumerate(appointments_data)
    if a[6] in ("Completed", "In Progress")
]

prescriptions_data = []
for appt_id, appt in eligible_appointments:
    if random.random() > 0.6:
        continue
    med_name = random.choice(list(medications.keys()))
    med_info = medications[med_name]
    dosage = random.choice(med_info["dosages"])
    freq = random.choices(frequencies, weights=freq_weights, k=1)[0]
    duration = random.choice(med_info["durations"])
    prescribed_date = appt[3]
    prescriptions_data.append((appt_id, appt[0], appt[1], med_name,
                               dosage, freq, duration, prescribed_date))

cursor.executemany(
    """INSERT INTO prescriptions (appointment_id, patient_id, doctor_id,
       medication_name, dosage_mg, frequency, duration_days, prescribed_date)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
    prescriptions_data
)
print(f"Inserted {len(prescriptions_data)} prescriptions.")

payment_methods = ["Cash", "Credit Card", "Debit Card", "Insurance",
                   "NHS Funded", "Bank Transfer"]
pay_method_weights = [5, 10, 10, 15, 55, 5]

payment_statuses = ["Pending", "Partially Paid", "Paid", "Overdue", "Refunded"]
pay_status_weights = [10, 5, 70, 10, 5]

triage_cost_map = {
    "Non-Urgent": (50, 150),
    "Standard":   (100, 300),
    "Urgent":     (200, 500),
    "Emergency":  (500, 1500),
    "Critical":   (1000, 5000),
}

billing_data = []
completed_appointments = [
    (i + 1, a) for i, a in enumerate(appointments_data)
    if a[6] in ("Completed", "In Progress", "Checked-In")
]

for appt_id, appt in completed_appointments:
    triage = appt[5]
    cost_range = triage_cost_map[triage]
    bill_amount = round(random.uniform(cost_range[0], cost_range[1]), 2)
    pay_method = random.choices(payment_methods, weights=pay_method_weights, k=1)[0]
    pay_status = random.choices(payment_statuses, weights=pay_status_weights, k=1)[0]

    if pay_method == "NHS Funded":
        bill_amount = round(bill_amount * random.choice([0, 0, 0, 0.1, 0.2]), 2)
        if bill_amount == 0:
            pay_status = "Paid"

    billing_date = appt[3]
    billing_data.append((appt[0], appt_id, bill_amount, pay_method,
                         pay_status, billing_date))

cursor.executemany(
    """INSERT INTO billing (patient_id, appointment_id, bill_amount,
       payment_method, payment_status, billing_date)
       VALUES (?, ?, ?, ?, ?, ?)""",
    billing_data
)
print(f"Inserted {len(billing_data)} billing records.")

conn.commit()

print("\n" + "=" * 60)
print("DATABASE GENERATION COMPLETE")
print("=" * 60)

tables = ["departments", "doctors", "patients", "appointments",
          "prescriptions", "billing"]

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"  {table:20s}: {count:>6,} rows")

conn.close()
print(f"\nDatabase saved as: {DB_NAME}")
