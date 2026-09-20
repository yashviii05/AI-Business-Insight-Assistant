"""
logger.py
---------
Phase 5, Steps 1-2: Track every question asked, whether it worked,
and how long it took — so you can calculate a real metric later,
like "generated valid SQL 90% of the time."
"""

import csv
import os
import time
from datetime import datetime

LOG_FILE = "query_log.csv"


def log_query(question: str, sql_query: str, success: bool, elapsed_seconds: float):
    """
    Appends one row to query_log.csv for every question asked.
    Creates the file with headers if it doesn't exist yet.
    """
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "question", "sql_query", "success", "seconds_taken"])
        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            question,
            sql_query,
            success,
            round(elapsed_seconds, 2),
        ])


def calculate_success_rate() -> float:
    """
    Step 2: Reads the log file and returns the percentage of
    questions that produced valid, runnable SQL.
    """
    if not os.path.isfile(LOG_FILE):
        return 0.0

    with open(LOG_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        return 0.0

    successes = sum(1 for row in rows if row["success"] == "True")
    return round((successes / len(rows)) * 100, 1)


if __name__ == "__main__":
    print(f"Current success rate: {calculate_success_rate()}%")
