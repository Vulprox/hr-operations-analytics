-- A date spine keeps empty months visible; the last month is capped at the reporting date.
WITH RECURSIVE months(month_start) AS (
  SELECT date(:report_date, 'start of year')
  UNION ALL
  SELECT date(month_start, '+1 month') FROM months
  WHERE date(month_start, '+1 month') <= :report_date
), cuts AS (
  SELECT month_start, MIN(date(month_start, '+1 month', '-1 day'), :report_date) AS as_of
  FROM months
), companies AS (SELECT DISTINCT company FROM employees)
SELECT c.month_start, c.as_of, co.company, COUNT(e.employee_id) AS active_employees
FROM cuts c CROSS JOIN companies co
LEFT JOIN employees e ON e.company=co.company AND e.start_date<=c.as_of
 AND (e.end_date IS NULL OR e.end_date>=c.as_of)
GROUP BY c.month_start,c.as_of,co.company
ORDER BY c.month_start,co.company;
