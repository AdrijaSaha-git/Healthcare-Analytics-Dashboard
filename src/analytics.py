"""
Analytics helper functions for the Healthcare Analytics Dashboard.

KPIs:
- Test volume trends
- Abnormal rate
- Turn-around-time (TAT)
- Technician performance
"""

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path


# ---------------------- DB CONNECTION & DATA LOAD ---------------------- #

def get_connection():
    """to create and return a MySQL connection to healthcare_analytics."""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",              
        password="sqlsqlsql",  
        database="healthcare_analytics"
    )
    return conn


def load_joined_results() -> pd.DataFrame:
    """
    Joining test_orders, test_results, patients, and technicians
    into a single DataFrame for analysis.
    """
    conn = get_connection()
    query = """
        SELECT
            r.result_id,
            p.patient_code,
            o.order_id,
            o.ordered_at,
            o.priority,
            r.test_name,
            r.result_value,
            r.reference_low,
            r.reference_high,
            r.result_time,
            t.tech_id,
            t.tech_name
        FROM test_results r
        JOIN test_orders o ON r.order_id = o.order_id
        JOIN patients p ON o.patient_id = p.patient_id
        JOIN technicians t ON r.tech_id = t.tech_id;
    """
    df = pd.read_sql(query, conn)
    conn.close()

    df["ordered_at"] = pd.to_datetime(df["ordered_at"])
    df["result_time"] = pd.to_datetime(df["result_time"])
    df["date"] = df["ordered_at"].dt.date

    # TAT in hours
    df["tat_hours"] = (df["result_time"] - df["ordered_at"]).dt.total_seconds() / 3600

    # Abnormal flag
    df["is_abnormal"] = (
        (df["result_value"] < df["reference_low"]) |
        (df["result_value"] > df["reference_high"])
    )

    return df


# ----------------------------- KPI FUNCTIONS ---------------------------- #

def test_volume_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Number of tests per day."""
    return df.groupby("date").agg(test_count=("result_id", "count")).reset_index()


def abnormal_rate(df: pd.DataFrame) -> pd.DataFrame:
    """Abnormal rate per day."""
    daily = df.groupby("date").agg(
        total_tests=("result_id", "count"),
        abnormal_tests=("is_abnormal", "sum")
    ).reset_index()
    daily["abnormal_pct"] = daily["abnormal_tests"] / daily["total_tests"] * 100
    return daily


def tat_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Average TAT per day (hours)."""
    return df.groupby("date").agg(
        avg_tat_hours=("tat_hours", "mean")
    ).reset_index()


def technician_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Technician performance summary:
    - total tests done
    - % abnormal
    - average TAT
    """
    grp = df.groupby(["tech_id", "tech_name"]).agg(
        tests_done=("result_id", "count"),
        abnormal_pct=("is_abnormal", lambda x: x.mean() * 100),
        avg_tat_hours=("tat_hours", "mean")
    ).reset_index()
    return grp


# ---------------------------- DASHBOARD (PLOTS) ------------------------- #

def create_dashboard(df: pd.DataFrame, output_pdf: Path):
    """
    For creating a simple PDF dashboard with:
    - Test volume trend
    - Abnormal rate trend
    - Average TAT trend
    - Technician performance (bar chart)
    """
    vol = test_volume_trend(df)
    abn = abnormal_rate(df)
    tat = tat_summary(df)
    tech = technician_performance(df)

    with PdfPages(output_pdf) as pdf:

        # Test volume trend
        fig1, ax1 = plt.subplots()
        ax1.plot(vol["date"], vol["test_count"], marker="o")
        ax1.set_title("Test Volume per Day")
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Number of Tests")
        pdf.savefig(fig1)
        plt.close(fig1)

        # Abnormal rate
        fig2, ax2 = plt.subplots()
        ax2.plot(abn["date"], abn["abnormal_pct"], marker="o")
        ax2.set_title("Abnormal Rate per Day")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Abnormal (%)")
        pdf.savefig(fig2)
        plt.close(fig2)

        # TAT trend
        fig3, ax3 = plt.subplots()
        ax3.plot(tat["date"], tat["avg_tat_hours"], marker="o")
        ax3.set_title("Average TAT per Day")
        ax3.set_xlabel("Date")
        ax3.set_ylabel("TAT (hours)")
        pdf.savefig(fig3)
        plt.close(fig3)

        # Technician performance
        fig4, ax4 = plt.subplots()
        ax4.bar(tech["tech_name"], tech["tests_done"])
        ax4.set_title("Technician Performance – Tests Done")
        ax4.set_ylabel("Number of Tests")
        pdf.savefig(fig4)
        plt.close(fig4)
