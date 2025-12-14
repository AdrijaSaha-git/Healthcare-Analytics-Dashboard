"""
Healthcare Analytics Dashboard – Patient & Test Trends

Runs end-to-end KPIs:
- Test volume trends
- Abnormal rate
- Turn-around-time
- Technician performance
And generates a PDF dashboard.
"""

from pathlib import Path
from analytics import load_joined_results, create_dashboard, technician_performance


def main():
    project_root = Path(__file__).resolve().parents[1]
    reports_dir = project_root / "reports"
    reports_dir.mkdir(exist_ok=True)

    print("Loading data from MySQL...")
    df = load_joined_results()
    print("\nSample of joined data:")
    print(df.head())

    # Show technician KPI table in console
    print("\nTechnician performance summary:")
    tech_summary = technician_performance(df)
    print(tech_summary)

    # Dashboard
    pdf_path = reports_dir / "healthcare_kpi_dashboard.pdf"
    print("\nGenerating dashboard PDF...")
    create_dashboard(df, pdf_path)
    print(f"Dashboard saved to: {pdf_path}")


if __name__ == "__main__":
    main()
