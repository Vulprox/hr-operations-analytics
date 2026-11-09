"""Independent reconciliations and boundary fixtures for the synthetic release."""
import csv
from datetime import date,timedelta
import importlib.util
import io
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from run_analysis import load_database,query,records,REPORT_DATE

class PortfolioTests(unittest.TestCase):
    def setUp(self): self.db=load_database()
    def tearDown(self): self.db.close()

    def test_release_sizes(self):
        for table,count in [('employees',100),('apartments',10),('stays',100),('absences',165),('leave_periods',185)]:
            with self.subTest(table=table): self.assertEqual(self.db.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0],count)

    def test_foreign_keys(self):
        self.assertEqual(self.db.execute('PRAGMA foreign_key_check').fetchall(),[])

    def test_duplicate_employee_rejected(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute('INSERT INTO employees SELECT * FROM employees LIMIT 1')

    def test_missing_employee_rejected(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("INSERT INTO absences VALUES ('TEST','MISSING','2026-01-01','2026-01-02','OK')")

    def test_reversed_absence_rejected(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("INSERT INTO absences VALUES ('TEST','EMP-0001','2026-01-02','2026-01-01','OK')")

    def test_headcount_reconciles(self):
        actual={r['company']:r['active_employees'] for r in query(self.db,'01_headcount.sql')}
        expected={}
        for r in records('employees'):
            if r['Start date']<=REPORT_DATE and (not r['Termination date'] or r['Termination date']>=REPORT_DATE):
                expected[r['Company']]=expected.get(r['Company'],0)+1
        self.assertEqual(actual,expected);self.assertEqual(sum(actual.values()),85)

    def test_employment_final_day_included(self):
        self.db.execute("INSERT INTO employees VALUES ('TEST','Boundary company','2026-10-28','2026-10-28')")
        today={r['company']:r['active_employees'] for r in query(self.db,'01_headcount.sql')}
        tomorrow={r['company']:r['active_employees'] for r in query(self.db,'01_headcount.sql','2026-10-29')}
        self.assertEqual(today['Boundary company'],1);self.assertEqual(tomorrow['Boundary company'],0)

    def test_monthly_headcount_last_cut(self):
        rows=query(self.db,'02_monthly_headcount.sql')
        self.assertEqual(len(rows),20)
        self.assertEqual(sum(r['active_employees'] for r in rows[-2:]),85)
        self.assertTrue(all(r['as_of']==REPORT_DATE for r in rows[-2:]))

    def test_housing_snapshot_reconciles(self):
        expected={r['ApartmentID']:int(r['Residents on reporting date']) for r in records('apartments')}
        actual={r['apartment_id']:r['residents'] for r in query(self.db,'03_housing_occupancy.sql')}
        self.assertEqual(actual,expected);self.assertEqual(sum(actual.values()),40)

    def test_move_day_not_double_counted(self):
        self.db.execute('DELETE FROM stays')
        self.db.executemany('INSERT INTO stays VALUES (?,?,?,?,?,?)',[
          ('T1','EMP-0001','APT-01','2026-10-01','2026-10-28','OK'),
          ('T2','EMP-0001','APT-02','2026-10-28',None,'OK')])
        r={x['apartment_id']:x['residents'] for x in query(self.db,'03_housing_occupancy.sql')}
        self.assertEqual((r['APT-01'],r['APT-02']),(0,1))

    def test_invalid_stay_excluded(self):
        before=[tuple(r) for r in query(self.db,'03_housing_occupancy.sql')]
        self.db.execute("INSERT INTO stays VALUES ('TEST','EMP-0100','APT-01','2026-10-01',NULL,'Overlapping stay')")
        self.assertEqual(before,[tuple(r) for r in query(self.db,'03_housing_occupancy.sql')])

    def test_sickness_duration_and_employment(self):
        employees={r['EmployeeID']:r for r in records('employees')}
        for r in records('sick_leave'):
            start=date.fromisoformat(r['Start date']);end=date.fromisoformat(r['End date'])
            self.assertEqual(int(r['Calendar days']),(end-start).days+1)
            emp=employees[r['EmployeeID']]
            self.assertGreaterEqual(r['Start date'],emp['Start date'])
            if emp['Termination date']: self.assertLessEqual(r['End date'],emp['Termination date'])

    def test_no_overlaps_in_release(self):
        for source,begin,end,exclusive in [('sick_leave','Start date','End date',False),('leave','Start date','End date',False),('stays','Check-in date','Check-out date (exclusive)',True)]:
            groups={}
            for r in records(source): groups.setdefault(r['EmployeeID'],[]).append(r)
            for rows in groups.values():
                rows.sort(key=lambda r:r[begin])
                for a,b in zip(rows,rows[1:]):
                    stop=a[end] or '9999-12-31'
                    self.assertTrue(stop<=b[begin] if exclusive else stop<b[begin],source)

    def test_monthly_absence_independent_daily_allocation(self):
        expected={f'2026-{m:02d}-01':[0,0] for m in range(1,11)}
        cutoff=date.fromisoformat(REPORT_DATE)
        for r in records('sick_leave'):
            if r['Validation']!='OK':continue
            start=date.fromisoformat(r['Start date']);end=min(date.fromisoformat(r['End date']),cutoff)
            key=start.replace(day=1).isoformat()
            if key in expected and start<=cutoff:expected[key][0]+=1
            d=max(start,date(2026,1,1))
            while d<=end:
                expected[d.replace(day=1).isoformat()][1]+=1;d+=timedelta(days=1)
        actual={r['month_start']:[r['episodes_started'],r['calendar_absence_days']] for r in query(self.db,'04_monthly_absence.sql')}
        self.assertEqual(actual,expected)

    def test_cross_month_absence_and_reporting_cap(self):
        self.db.execute('DELETE FROM absences')
        self.db.execute("INSERT INTO absences VALUES ('TEST','EMP-0001','2026-01-30','2026-02-04','OK')")
        r=query(self.db,'04_monthly_absence.sql','2026-02-02')
        self.assertEqual([(x['episodes_started'],x['calendar_absence_days']) for x in r],[(1,2),(0,2)])

    def test_leave_balances_reconcile_to_native_snapshot(self):
        native={r['EmployeeID']:r for r in records('leave_balances')}
        for r in query(self.db,'05_leave_balances.sql'):
            n=native[r['employee_id']]
            for a,b in [('accrued_hours','Accrued hours'),('deducted_hours','Deducted hours'),('remaining_hours','Remaining hours'),('remaining_days','Remaining days'),('future_reserved_hours','Future reserved hours'),('available_after_reservations','Available after reservations')]:
                self.assertAlmostEqual(float(r[a]),float(n[b]),places=2,msg=f'{r["employee_id"]}: {a}')

    def test_invalid_leave_not_deducted(self):
        before=[tuple(r) for r in query(self.db,'05_leave_balances.sql')]
        self.db.execute("INSERT INTO leave_periods VALUES ('TEST','EMP-0001','2026-10-01','2026-10-05',40,'Overlapping leave')")
        self.assertEqual(before,[tuple(r) for r in query(self.db,'05_leave_balances.sql')])

    def test_future_leave_reserved(self):
        self.db.execute('DELETE FROM leave_periods')
        self.db.execute("INSERT INTO leave_periods VALUES ('TEST','EMP-0001','2026-11-01','2026-11-05',40,'OK')")
        row=next(r for r in query(self.db,'05_leave_balances.sql') if r['employee_id']=='EMP-0001')
        self.assertEqual(row['deducted_hours'],0);self.assertEqual(row['future_reserved_hours'],40)

class ReferenceInputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location('generate_reference',ROOT/'projects/employee-references/generate_reference.py')
        cls.module=importlib.util.module_from_spec(spec)
        try:spec.loader.exec_module(cls.module)
        except ModuleNotFoundError as e:raise unittest.SkipTest(f'Optional PDF dependency unavailable: {e}')

    def test_missing_id_rejected(self):
        with self.assertRaises(ValueError):self.module.load_employee(ROOT/'data/employee_references.csv','MISSING')

    def test_not_synthetic_rejected(self):
        row=records('employee_references')[0];row['data_classification']='NOT SYNTHETIC'
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'input.csv'
            with p.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=row.keys());w.writeheader();w.writerow(row)
            with self.assertRaises(ValueError):self.module.load_employee(p,row['EmployeeID'])

    def test_duplicate_reference_rejected(self):
        row=records('employee_references')[0]
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'input.csv'
            with p.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=row.keys());w.writeheader();w.writerows([row,row])
            with self.assertRaises(ValueError):self.module.load_employee(p,row['EmployeeID'])

if __name__=='__main__':unittest.main()
