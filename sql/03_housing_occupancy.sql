-- Check-out is exclusive. COUNT(DISTINCT) is an additional guard, not a replacement for validation.
SELECT a.apartment_id, a.capacity, COUNT(DISTINCT s.employee_id) AS residents,
       a.capacity - COUNT(DISTINCT s.employee_id) AS available_beds,
       ROUND(1.0 * COUNT(DISTINCT s.employee_id) / a.capacity, 3) AS occupancy_rate,
       CASE WHEN COUNT(DISTINCT s.employee_id)>a.capacity THEN 'Over capacity' ELSE 'OK' END AS capacity_check
FROM apartments a
LEFT JOIN stays s ON s.apartment_id=a.apartment_id AND s.validation='OK'
 AND s.check_in<=:report_date AND (s.check_out IS NULL OR s.check_out>:report_date)
WHERE a.rental_start<=:report_date AND (a.rental_end IS NULL OR a.rental_end>=:report_date)
GROUP BY a.apartment_id,a.capacity ORDER BY a.apartment_id;
