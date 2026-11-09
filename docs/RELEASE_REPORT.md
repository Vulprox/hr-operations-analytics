# Portfolio preparation report

**Author:** Yakiv Petrov. **Release:** 2026-10-28.

## Outcome

The package is prepared for repository upload as an English-language HR operations analytics portfolio. It combines real workplace problem context with entirely fictional publication data. Four native publication copies were prepared while preserving the original online files. GitHub publication and public Google sharing have not been performed.

## Completed work

| Area | Change | Evidence |
|---|---|---|
| Provenance | Clear separation of workplace contribution, fictional data and AI-assisted reconstruction | Root README and METHODS |
| Imports | Replaced failing cross-file imports with explicit local snapshot references | No IMPORTRANGE in released exports |
| Dates | Set release defaults to 2026-10-28; fixed employee status/tenure for reproducibility | Native controls and exported values |
| Leave | Excluded invalid records from deductions/reserves; added per-employee warnings | Native overlap fixture, SQL reconciliation |
| Housing | Excluded invalid stays from apartment totals, resident lists and 12 calendars | Native overlap fixture and move-day test |
| Language | Translated residual Russian formula messages and conditional-format values; planned marker is P | Exported XML language scan |
| Navigation | Added Read Me pages and a five-minute repository review path | Native copies and README |
| SQL | Added five queries, typed relational schema, CLI runner and committed results | sql/, scripts/, examples/sql-results/ |
| Verification | Added 21 tests, release-integrity checker and CI configuration | tests/ and .github/workflows/validate.yml |
| PDF automation | Tightened synthetic classification and required/date-field validation | Reference input tests |
| Presentation | Rebuilt reporting images, replaced empty leave PNG and added overview/housing charts | assets/ |

## Verified results

- 100 unique employees: 85 active and 15 former at the release date.
- Active headcount: 43 and 42 across two fictional companies.
- 10 apartments, 100 stay records and 40 current residents.
- 185 leave periods; all 100 calculated balances reconciled with native snapshots to 0.01.
- 165 sickness periods; durations and employment boundaries checked.
- 74 sickness episodes started in 2026 through October 28; 647 calendar absence days allocated to January-October.
- July: zero new episodes and ten absence days. October: six episodes and 28 elapsed days.
- All 21 tests passed with ReportLab installed. The SQL workflow completed locally.

## Native negative tests

Two leave periods were temporarily changed to overlap. Both were flagged; EMP-0001 deductions changed from 64 to 0 and the balance showed an exclusion warning. Restoring the dates restored 64 hours and OK statuses.

A stay was temporarily reassigned to overlap another stay. Both were flagged; APT-01 occupancy changed from four to three. Restoring the employee restored four residents and OK statuses. No fixture data remains in the release.

## Positioning

The strongest evidence is the connection between operational requirements, record design, date logic, reusable reporting and verification. Employee Management provides an accessible introduction; Housing demonstrates interval modeling; SQL makes the analysis reproducible; the PDF script adds document automation.

The SQL module is a portfolio extension developed with AI assistance, not a historical workplace deployment. Interview explanations should focus on decisions the author can explain, then demonstrate one query and one boundary test. This release does not claim Power BI experience, production database deployment or a measured error-reduction rate.

## Known limits

- The native Google-rendered visual review was blocked by a sign-in requirement. Export/connector inspection and local publication previews were reviewed; full native visual parity is not certified.
- XLSX exports retain Google-specific constructs and are not certified for Excel recalculation.
- Native copies use separate snapshots; no live synchronization is claimed.
- Company summary ranges support two configured employers; housing calendars cover 2026.
- Employment assumes one interval per employee; holidays, shifts and rehire/transfer histories are not modeled.
- The example leave log contains 2026 consumption while accrual spans employment. Values demonstrate mechanics, not real entitlement or liabilities. Duration diversity is deliberately limited in the supplied sample.
- SQL consumes validation statuses; independent tests cover the supplied release and selected fixtures, not all arbitrary replacement inputs.
- Reported workplace time savings remain the author's observations, not controlled benchmarks.

## Publication steps

1. Create `hr-operations-analytics` and upload the repository folder contents, including hidden workflow files.
2. Inspect the first hosted GitHub Actions run and README rendering.
3. Pin the repository; use the project cases to support relevant CV statements.
4. Optionally enable viewer access to the synthetic native copies and test signed-out access before advertising live demos.
5. Choose a reuse license if desired. None was selected on the author's behalf.

See [PUBLISHING.md](../PUBLISHING.md), [native copy links](ONLINE_DEMOS.md), [methods](METHODS.md) and [verification](VALIDATION.md).
