-- Demo policy: 13.36 hours per COMPLETE month, 8 hours/day; no expiry/carryover model.
-- All paid hours of a valid period are charged on its start date.
WITH cutoffs AS (
 SELECT *,MIN(COALESCE(end_date,:report_date),:report_date) AS cutoff FROM employees
), accrual AS (
 SELECT *,MAX(0,
  (CAST(strftime('%Y',cutoff) AS INTEGER)-CAST(strftime('%Y',start_date) AS INTEGER))*12
  +CAST(strftime('%m',cutoff) AS INTEGER)-CAST(strftime('%m',start_date) AS INTEGER)
  -(CAST(strftime('%d',cutoff) AS INTEGER)<CAST(strftime('%d',start_date) AS INTEGER))
 )*13.36 AS accrued_hours FROM cutoffs
), balances AS (
 SELECT e.employee_id,e.company,e.accrued_hours,
  COALESCE(SUM(CASE WHEN l.start_date BETWEEN e.start_date AND e.cutoff THEN l.paid_hours ELSE 0 END),0) AS deducted_hours,
  COALESCE(SUM(CASE WHEN l.start_date>:report_date THEN l.paid_hours ELSE 0 END),0) AS future_reserved_hours
 FROM accrual e LEFT JOIN leave_periods l ON l.employee_id=e.employee_id AND l.validation='OK'
 GROUP BY e.employee_id,e.company,e.accrued_hours
)
SELECT employee_id,company,ROUND(accrued_hours,2) AS accrued_hours,deducted_hours,
 ROUND(accrued_hours-deducted_hours,2) AS remaining_hours,
 ROUND((accrued_hours-deducted_hours)/8,2) AS remaining_days,
 future_reserved_hours,ROUND(accrued_hours-deducted_hours-future_reserved_hours,2) AS available_after_reservations
FROM balances ORDER BY employee_id;
