PRAGMA foreign_keys = ON;
CREATE TABLE employees (
  employee_id TEXT PRIMARY KEY, company TEXT NOT NULL,
  start_date TEXT NOT NULL, end_date TEXT,
  CHECK(end_date IS NULL OR end_date >= start_date)
);
CREATE TABLE apartments (
  apartment_id TEXT PRIMARY KEY, capacity INTEGER NOT NULL CHECK(capacity > 0),
  rental_start TEXT NOT NULL, rental_end TEXT
);
CREATE TABLE stays (
  stay_id TEXT PRIMARY KEY, employee_id TEXT NOT NULL REFERENCES employees,
  apartment_id TEXT NOT NULL REFERENCES apartments,
  check_in TEXT NOT NULL, check_out TEXT, validation TEXT NOT NULL,
  CHECK(check_out IS NULL OR check_out > check_in)
);
CREATE TABLE absences (
  absence_id TEXT PRIMARY KEY, employee_id TEXT NOT NULL REFERENCES employees,
  start_date TEXT NOT NULL, end_date TEXT NOT NULL, validation TEXT NOT NULL,
  CHECK(end_date >= start_date)
);
CREATE TABLE leave_periods (
  leave_id TEXT PRIMARY KEY, employee_id TEXT NOT NULL REFERENCES employees,
  start_date TEXT NOT NULL, end_date TEXT NOT NULL,
  paid_hours REAL NOT NULL CHECK(paid_hours >= 0), validation TEXT NOT NULL,
  CHECK(end_date >= start_date)
);
CREATE INDEX stays_employee_dates ON stays(employee_id, check_in, check_out);
CREATE INDEX absences_employee_dates ON absences(employee_id, start_date, end_date);
CREATE INDEX leave_employee_dates ON leave_periods(employee_id, start_date, end_date);
