"""Load the synthetic CSV release into SQLite and run parameterized reports.

Python standard library only. Does not access Google, workplace systems or a network.
"""
from __future__ import annotations
import argparse
import csv
from datetime import date
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
REPORT_DATE = '2026-10-28'

def records(name: str, root: Path = ROOT) -> list[dict[str, str]]:
    with (root/'data'/f'{name}.csv').open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))

def load_database(root: Path = ROOT) -> sqlite3.Connection:
    db=sqlite3.connect(':memory:')
    db.row_factory=sqlite3.Row
    db.executescript((root/'sql/schema.sql').read_text())
    specs=[
      ('employees','employees',['EmployeeID','Company','Start date','Termination date']),
      ('apartments','apartments',['ApartmentID','Capacity','Rental start','Rental end']),
      ('stays','stays',['StayID','EmployeeID','ApartmentID','Check-in date','Check-out date (exclusive)','Validation']),
      ('absences','sick_leave',['AbsenceID','EmployeeID','Start date','End date','Validation']),
      ('leave_periods','leave',['LeaveID','EmployeeID','Start date','End date','Paid hours','Validation'])
    ]
    for table,source,fields in specs:
        rows=records(source,root)
        # Validate date syntax before SQLite's lexicographic date comparisons.
        for row in rows:
            for key in fields:
                if ('date' in key.lower() or key in ('Rental start','Rental end')) and row[key]:
                    date.fromisoformat(row[key])
        db.executemany(f'INSERT INTO {table} VALUES ({",".join("?" for _ in fields)})',
                       [[r[k] if r[k]!='' else None for k in fields] for r in rows])
    db.commit()
    return db

def query(db: sqlite3.Connection, name: str, report_date: str = REPORT_DATE):
    date.fromisoformat(report_date)
    return db.execute((ROOT/'sql'/name).read_text(),{'report_date':report_date}).fetchall()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--report-date',default=REPORT_DATE)
    p.add_argument('--output-dir',type=Path,default=ROOT/'outputs')
    args=p.parse_args(); date.fromisoformat(args.report_date)
    args.output_dir.mkdir(parents=True,exist_ok=True)
    with load_database() as db:
        for sql in sorted((ROOT/'sql').glob('[0-9]*.sql')):
            rows=query(db,sql.name,args.report_date)
            target=args.output_dir/(sql.stem+'.csv')
            with target.open('w',newline='',encoding='utf-8') as f:
                if rows:
                    w=csv.writer(f);w.writerow(rows[0].keys());w.writerows(rows)
            print(f'{sql.stem}: {len(rows)} rows -> {target}')

if __name__=='__main__': main()
