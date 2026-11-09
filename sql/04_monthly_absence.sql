-- Cases are assigned to their start month; days are allocated to every overlapping month.
WITH RECURSIVE months(month_start) AS (
  SELECT date(:report_date,'start of year')
  UNION ALL SELECT date(month_start,'+1 month') FROM months
  WHERE date(month_start,'+1 month')<=:report_date
), bounds AS (
  SELECT month_start,MIN(date(month_start,'+1 month','-1 day'),:report_date) AS month_end FROM months
)
SELECT b.month_start,
       SUM(CASE WHEN a.start_date BETWEEN b.month_start AND b.month_end THEN 1 ELSE 0 END) AS episodes_started,
       CAST(COALESCE(SUM(julianday(MIN(a.end_date,b.month_end))-
           julianday(MAX(a.start_date,b.month_start))+1),0) AS INTEGER) AS calendar_absence_days
FROM bounds b
LEFT JOIN absences a ON a.validation='OK' AND a.start_date<=b.month_end AND a.end_date>=b.month_start
GROUP BY b.month_start ORDER BY b.month_start;
