# Explaining the portfolio

## Introduction

My HR work involved recurring requests about employees, accommodation, leave and absence. I designed spreadsheets that organized records and reused calculation rules instead of rebuilding each answer. This portfolio reconstructs those workflows with fictional data and adds a reproducible SQL analysis layer.

## Questions to prepare

1. **Why EmployeeID?** Names may change or repeat. IDs connect events to the correct person; SQL enforces primary and foreign keys.
2. **Why exclusive checkout?** A move ends the old stay and starts the new stay without counting the person twice that day.
3. **Why separate cases and days?** One period starts once but can contribute days to multiple months. July demonstrates this.
4. **How are bad inputs handled?** Flag them, exclude them consistently and show a warning. Both overlapping intervals are excluded until corrected.
5. **Why freeze the date?** Reviewers can reproduce the same release later. Editable reporting controls are documented separately.
6. **How is SQL checked?** Reconcile against workbook snapshots and an independent calculation, then test boundaries.
7. **What did AI do?** It assisted reconstruction, implementation, documentation, SQL and checks. Explain the decisions you made and the code you can walk through.
8. **What comes next?** Rehire/transfer history, source refresh, work calendars and broader input coverage.

Start with a headcount query, explain the date boundary, show a same-day housing move, then walk through the cross-month sickness test. Use PDF generation as a supplementary automation example.

Before adding SQL to a CV skills section, practice changing the date, explaining each join/CTE and predicting boundary-test results. This repository supports that practice; it does not itself establish proficiency.
