# Hospital Management System - SQLite Database

A SQLite database with 6 related tables and a Python data generator for a hospital management system.

## How to Run

1. Clone the repository:
```bash
git clone <your-repo-url>
cd sql_database_project
```

2. Run the script:
```bash
python3 generate_hospital_db.py
```

This will automatically install required packages if missing and generate `hospital_management.db`.

## Project Structure

- `schema.sql` - SQL file that creates all 6 tables with constraints and foreign keys
- `generate_hospital_db.py` - Python script that populates the database with randomised data
- `requirements.txt` - Python dependencies
- `hospital_management.db` - Generated SQLite database

## Database Tables

| Table | Rows | Description |
|-------|------|-------------|
| departments | 10 | Hospital departments |
| doctors | 50 | Medical staff linked to departments |
| patients | 1,500 | Patient records |
| appointments | 2,000 | Patient-doctor appointments |
| prescriptions | 879 | Medications prescribed |
| billing | 1,590 | Payment records |

## Requirements

- Python 3.11+
- Faker (auto-installed when you run the script)
