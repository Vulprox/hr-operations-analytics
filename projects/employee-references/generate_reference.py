"""Generate an English reference PDF from the local synthetic portfolio CSV."""
from __future__ import annotations

import reportlab
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import argparse
import csv
from datetime import date
from pathlib import Path
import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

ROOT = Path(__file__).resolve().parents[2]


def load_employee(csv_path: Path, employee_id: str) -> dict[str, str]:
    with csv_path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"EmployeeID", "full_name", "employment_start_date", "termination_date", "data_classification"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError("Missing columns: " + ", ".join(sorted(missing)))
        matches = [row for row in reader if row["EmployeeID"].strip() == employee_id.strip()]
    if len(matches) != 1:
        raise ValueError(f"Expected one record for {employee_id!r}; found {len(matches)}.")
    if matches[0]["data_classification"].strip().upper() not in {"SYNTHETIC", "SYNTHETIC — PORTFOLIO ONLY"}:
        raise ValueError("This portfolio example accepts explicitly synthetic records only.")
    row = matches[0]
    for field in required:
        if not row[field].strip():
            raise ValueError(f"Required field is empty: {field}")
    start = date.fromisoformat(row["employment_start_date"])
    end = date.fromisoformat(row["termination_date"])
    if end < start:
        raise ValueError("Termination date precedes employment start.")
    return matches[0]


def build_pdf(row: dict[str, str], destination: Path) -> None:
    font_dir = Path(reportlab.__file__).resolve().parent / "fonts"
    pdfmetrics.registerFont(TTFont("PortfolioSans", str(font_dir / "Vera.ttf")))
    pdfmetrics.registerFont(TTFont("PortfolioSans-Bold", str(font_dir / "VeraBd.ttf")))
    pdfmetrics.registerFontFamily("PortfolioSans", normal="PortfolioSans", bold="PortfolioSans-Bold")
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="ReportTitle", fontName="PortfolioSans-Bold", fontSize=18,
                              leading=23, spaceAfter=7*mm, textColor=colors.HexColor("#203C34")))
    styles.add(ParagraphStyle(name="Field", fontName="PortfolioSans", fontSize=10,
                              leading=15, spaceAfter=3*mm))
    styles.add(ParagraphStyle(name="Notice", fontName="PortfolioSans", fontSize=9,
                              leading=13, textColor=colors.HexColor("#555555")))
    def get(key: str) -> str:
        return row.get(key, "").strip() or "Not specified"
    fields = [
        ("Employee", get("full_name")),
        ("Employee ID", get("EmployeeID")),
        ("Employer", get("employer_company")),
        ("Employment period", f'{get("employment_start_date")} to {get("termination_date")}'),
        ("Calendar employment days", get("total_employment_days")),
        ("Scheduled weekdays (Mon-Fri)", get("total_working_days")),
        ("Recorded sick leave days", get("sick_leave_days")),
        ("Client company", get("client_company")),
        ("Site role", get("site_role")),
        ("Recorded productivity assessment", get("productivity_status")),
        ("Evaluating supervisor", get("evaluating_supervisor")),
        ("Recorded termination category", get("termination_reason")),
        ("Work notes", get("work_notes")),
        ("Employee comments", get("employee_comments")),
    ]
    story = [Paragraph("EMPLOYEE REFERENCE", styles["ReportTitle"]),
             Paragraph("SYNTHETIC PORTFOLIO EXAMPLE - NOT AN EMPLOYMENT DOCUMENT", styles["Notice"]),
             Spacer(1, 6*mm)]
    for label, value in fields:
        story.append(Paragraph(f"<b>{escape(label)}:</b> {escape(value)}", styles["Field"]))
    story.extend([Spacer(1, 5*mm), HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD3CF")),
                  Spacer(1, 4*mm), Paragraph(
                      "All individuals and assessments are fictional. Scheduled weekdays do not represent actual attendance. "
                      "This document formats the supplied record; it does not infer performance or generate an assessment.",
                      styles["Notice"])])
    destination.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(str(destination), pagesize=A4, leftMargin=21*mm, rightMargin=21*mm,
                                 topMargin=18*mm, bottomMargin=18*mm,
                                 title="Synthetic employee reference", author="Yakiv Petrov")
    document.build(story)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--employee-id", required=True)
    parser.add_argument("--csv", type=Path, default=ROOT / "data" / "employee_references.csv")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        row = load_employee(args.csv, args.employee_id)
        safe_id = re.sub(r"[^A-Za-z0-9_-]", "_", args.employee_id)
        destination = args.output or Path(__file__).parent / "generated" / f"{safe_id}_reference.pdf"
        build_pdf(row, destination)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")
    print(f"Created: {destination}")


if __name__ == "__main__":
    main()
