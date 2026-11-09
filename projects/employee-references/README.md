# Employee Reference PDF

**From a structured employee record to a consistent document.**

In my workplace workflow, assessment information is collected in a table and a Python script creates an employee reference PDF when requested. This avoids manually copying the same fields into a new document layout each time.

This publication example adapts that workflow to an English, local-only synthetic dataset. It has no connection to the original workplace form or publicly exported personnel CSV.

## What the example does

1. Reads the included `employee_references.csv`.
2. Selects a single record by EmployeeID.
3. Rejects missing columns, missing IDs and duplicate matches.
4. Requires a synthetic-data classification.
5. Escapes text before inserting it into ReportLab paragraphs.
6. Creates an A4 PDF with consistent labels and a synthetic-data notice.

The script formats an existing record. It does not invent an employee assessment or automatically retrieve Google Form responses.

## Run from the repository root

Python 3.10 or newer is required. Install the dependency in a virtual environment if preferred.

```bash
python -m pip install -r projects/employee-references/requirements.txt
python projects/employee-references/generate_reference.py --employee-id EMP-0086
```

Select another ID from [the supplied CSV](../../data/employee_references.csv). Output defaults to `projects/employee-references/generated/`, which is excluded from Git tracking.

An explicit destination is also supported:

```bash
python projects/employee-references/generate_reference.py --employee-id EMP-0086 --output example.pdf
```

## Review the output

- [Sample PDF](examples/EMP-0086_reference.pdf)
- [PDF preview](../../assets/reference_pdf.png)
- [Python source](generate_reference.py)

The release uses standard-library CSV reading and ReportLab. It replaces the original hard-coded employee name, remote CSV URL and Windows-only font paths with a reproducible local example. The script embeds the Vera fonts bundled with ReportLab for consistent English rendering. Additional languages may require a font with broader character coverage.

The scheduled-weekday field is not actual attendance, and its separately generated sick-day example is not linked to the sick-leave module.
