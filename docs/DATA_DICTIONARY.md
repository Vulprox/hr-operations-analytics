# Data dictionary

All records are synthetic. Release snapshot: 2026-10-28. CSV files are UTF-8 value snapshots, not live connections. Dates use ISO YYYY-MM-DD for interchange; workbook display dates use MM/DD/YYYY. EmployeeID joins the modules.

## employees.csv

100 records. Columns in file order:

`EmployeeID`, `First name`, `Last name`, `Company`, `Start date`, `Termination date`, `Health insurer`, `Health insurance number`, `Social insurance number`, `Date of birth`, `Phone 1`, `Phone 2`, `Email`, `Employee name`, `Employment status`, `Registered address`, `Private residential address`.

## addresses.csv

85 records. Columns in file order:

`EmployeeID`, `Employee name`, `Registered address`, `Private residential address`.

## employee_references.csv

15 records. Columns in file order:

`EmployeeID`, `full_name`, `employer_company`, `employment_start_date`, `termination_date`, `total_employment_days`, `total_working_days`, `sick_leave_days`, `client_company`, `site_role`, `termination_reason`, `productivity_status`, `evaluating_supervisor`, `work_notes`, `employee_comments`, `recorded_at`, `data_classification`.

## apartments.csv

10 records. Columns in file order:

`ApartmentID`, `Address (fictional)`, `Capacity`, `Rental start`, `Rental end`, `Residents on reporting date`.

## stays.csv

100 records. Columns in file order:

`StayID`, `Employee name`, `EmployeeID`, `ApartmentID`, `Check-in date`, `Check-out date (exclusive)`, `Address`, `Company`, `Validation`, `Project site`, `Move reason`.

## residence.csv

40 records. Columns in file order:

`EmployeeID`, `Employee name`, `Company`, `Registered address`, `Actual residential address`, `Company housing`, `Registered at company housing`, `Validation`.

## leave.csv

185 records. Columns in file order:

`LeaveID`, `Employee name`, `EmployeeID`, `Start date`, `End date`, `Calendar days`, `Leave type`, `Paid hours`, `Payment status`, `Approval notes`, `Validation`.

## leave_balances.csv

100 records. Columns in file order:

`EmployeeID`, `Employee name`, `Company`, `Start date`, `Termination date`, `Accrued hours`, `Deducted hours`, `Remaining hours`, `Remaining days`, `Future reserved hours`, `Available after reservations`, `Validation`.

## sick_leave.csv

165 records. Columns in file order:

`AbsenceID`, `Employee name`, `Company`, `Start date`, `End date`, `Calendar days`, `Weekdays (Mon–Fri)`, `Certificate status`, `Period status`, `Expected return`, `Operational notes`, `Validation`, `Diagnosis`, `Clinic name`, `Clinic address`, `Doctor name`, `EmployeeID`.

## Interpretation

- `Scheduled weekdays` and `total_working_days` are Monday-Friday counts, not attendance or payroll hours.
- The references dataset contains independently authored fictional assessments; its sickness values are not reconciled to the separate sick-leave module.
- `Calendar days` includes both start and end dates for leave and sickness. Housing check-out is exclusive.
- An empty termination date means no recorded termination; it is not a date value of zero.
- Housing `Actual days` means scheduled occupancy through the reporting date, not independently verified physical presence.
- Leave accrual: 13.36 hours per complete month, 8 hours per day. Paid hours are manually supplied.
- Synthetic diagnoses are demonstration text, not medical advice or validated clinical records.
