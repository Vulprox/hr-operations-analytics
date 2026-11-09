# SQL analysis

**Reproduce operational reports from the same synthetic data as the spreadsheet demos.**

Added during portfolio preparation with AI assistance. This extends the original spreadsheet workflows and is not presented as a workplace SQL deployment.

```bash
python scripts/run_analysis.py --report-date 2026-10-28
```

Python's built-in `sqlite3` loads CSVs into an in-memory database with primary/foreign keys and date-order constraints. Five queries write CSVs to `outputs/`. No database server or network is required.

| Query | Question | Technique |
|---|---|---|
| [Headcount](../../sql/01_headcount.sql) | How many people are active in each company? | Conditional aggregation, inclusive boundary |
| [Monthly headcount](../../sql/02_monthly_headcount.sql) | How did headcount change this year? | Recursive date spine, cross join, left join |
| [Housing](../../sql/03_housing_occupancy.sql) | How many beds are occupied or available? | Interval join, distinct count, capacity check |
| [Monthly absence](../../sql/04_monthly_absence.sql) | How do cases differ from days absent? | Month intersections, cutoff, aggregation |
| [Leave balances](../../sql/05_leave_balances.sql) | Do accrual, deductions and reserves reconcile? | CTEs, complete-month arithmetic, conditional sums |

## Results to inspect

- Release headcount: **85, split 43 and 42** across the two employers.
- All 40 beds are occupied across ten apartments in this synthetic snapshot. The query retains empty apartments and flags over-capacity results.
- **July has zero new sickness episodes but ten absence days.** A period starting earlier continues into July.
- October has **six episodes and 28 elapsed absence days** through October 28; later days are excluded.

These describe fictional scenarios, not a real employer. See [saved results](../../examples/sql-results/) and [tests](../../tests/test_portfolio.py).

SQL consumes released validation statuses; it does not recreate every spreadsheet validation rule for arbitrary new data. Tests independently check this release. Housing SQL additionally limits output to apartments rented on the selected date. The leave model is a configured demo policy with incomplete synthetic historical consumption, not a real financial liability estimate.
