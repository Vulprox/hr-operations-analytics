-- One row per employer. The final employment day is included.
SELECT company,
       SUM(start_date <= :report_date AND (end_date IS NULL OR end_date >= :report_date)) AS active_employees,
       SUM(end_date < :report_date) AS former_employees,
       SUM(start_date > :report_date) AS not_started
FROM employees
GROUP BY company
ORDER BY company;
