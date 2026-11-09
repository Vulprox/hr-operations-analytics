# Verification

Release: **2026-10-28**. These are scoped checks, not certification of every possible input.

```bash
python -m pip install -r projects/employee-references/requirements.txt
python -m unittest discover -s tests -v
python scripts/check_release.py
python scripts/run_analysis.py --report-date 2026-10-28
```

The release passed **21 tests** with ReportLab installed. Without it, three PDF input tests are skipped. GitHub Actions is configured to install it; a hosted Actions run is not claimed before publication.

## Automated coverage

- Record counts, duplicate primary-key rejection and foreign-key integrity.
- Headcount reconciled to an independent date-based CSV calculation.
- Final employment day included; following day excluded.
- Monthly headcount cutoff and current total.
- Housing occupancy reconciled to native snapshot values.
- Exclusive checkout: a same-day move does not double-count a resident.
- Invalid stays and leave periods excluded from totals.
- All 165 sickness durations and employment boundaries checked.
- Independent overlap scans for stays, leave and sickness.
- Sickness days independently allocated day-by-day and reconciled with SQL.
- Cross-month sickness and reporting-date truncation.
- All 100 leave balances reconciled with native values, to 0.01.
- Future leave reserved separately.
- Missing/duplicate reference IDs and `NOT SYNTHETIC` classification rejected.

## Native Google Sheets fixtures

Tests ran in the publication copies. All temporary inputs were restored.

| Fixture | Observed result | After restoration |
|---|---|---|
| EMP-0001 leave periods changed to overlap | Both flagged; deductions 64 -> 0; balance warning shown | Both OK; deductions 64 |
| A stay reassigned to overlap EMP-0001 | Both flagged; APT-01 occupancy 4 -> 3 | Both OK; occupancy 4 |

External import formulas were removed. Exported XML was scanned for cached formula errors, residual Cyrillic text and IMPORTRANGE formulas. CSV counts and identifiers were checked after extraction.

## Visual and publication checks

Publication charts are rendered from released CSV/SQL results and labeled accordingly. They are not screenshots of original company files. The missing leave-dashboard image was replaced. Relative Markdown links, nonempty image/PDF files and workbook checksums are checked by `scripts/check_release.py`.

The browser requested Google sign-in, so a complete Google-rendered visual review was unavailable. Connector readback, native calculation checks, export inspection and local previews were used. Export is not proof of identical Excel recalculation. Anonymous online access remains a publication step; this repository runs without those links.
