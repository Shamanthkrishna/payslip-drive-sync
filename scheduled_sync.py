#!/usr/bin/env python3
"""
Scheduled monthly sync wrapper.

Behavior:
- Runs only within a configurable monthly day window (default: 6-12).
- Skips if this month already completed successfully.
- Retries failed sync attempts with delay.
- Persists last successful month in logs/sync_state.json.
"""

import json
import sys
import time
import logging
from datetime import datetime

from src.config import Config
from src.email_notifier import EmailNotifier
from sync_payslips import sync_all_payslips, setup_logging


STATE_FILE = Config.LOG_FOLDER / "sync_state.json"


def load_state():
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(state):
    Config.create_folders()
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def current_month_key():
    now = datetime.now()
    return f"{now.year:04d}-{now.month:02d}"


def should_run_today(window_start_day, window_end_day):
    day = datetime.now().day
    return window_start_day <= day <= window_end_day


def run_scheduled(max_months, attempts, retry_delay_minutes, window_start_day, window_end_day):
    logger = setup_logging()

    if not should_run_today(window_start_day, window_end_day):
        logger.info(
            f"Outside monthly run window ({window_start_day}-{window_end_day}). Skipping scheduled sync."
        )
        return 0

    state = load_state()
    month_key = current_month_key()

    if state.get("last_success_month") == month_key:
        logger.info(f"Scheduled sync already completed for {month_key}. Skipping.")
        return 0

    logger.info(
        f"Scheduled sync starting for {month_key} with {attempts} attempt(s), retry delay {retry_delay_minutes} min."
    )

    for attempt in range(1, attempts + 1):
        logger.info(f"Scheduled attempt {attempt}/{attempts}")
        success = sync_all_payslips(max_months=max_months)

        if success:
            state["last_success_month"] = month_key
            state["last_success_at"] = datetime.now().isoformat(timespec="seconds")
            save_state(state)
            logger.info(f"Scheduled sync succeeded for {month_key}")
            return 0

        if attempt < attempts:
            logger.warning(f"Attempt {attempt} failed. Retrying in {retry_delay_minutes} minute(s)...")
            time.sleep(retry_delay_minutes * 60)

    logger.error("Scheduled sync failed after all retry attempts")
    try:
        notifier = EmailNotifier()
        notifier.notify_error(
            f"Scheduled payslip sync failed after {attempts} attempt(s) for {month_key}.\n"
            f"Retry delay was {retry_delay_minutes} minute(s) between attempts.\n\n"
            f"Please check the logs or run sync_payslips.py manually.",
            month_year=month_key,
        )
    except Exception as email_err:
        logger.warning(f"Could not send failure notification email: {email_err}")
    return 1


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Scheduled monthly payslip sync runner")
    parser.add_argument("--max-months", type=int, default=24, help="Max months to check")
    parser.add_argument("--attempts", type=int, default=3, help="Retries per scheduled invocation")
    parser.add_argument("--retry-delay-min", type=int, default=20, help="Minutes between retries")
    parser.add_argument("--window-start-day", type=int, default=6, help="Monthly start day to run")
    parser.add_argument("--window-end-day", type=int, default=12, help="Monthly end day to run")

    args = parser.parse_args()

    code = run_scheduled(
        max_months=args.max_months,
        attempts=args.attempts,
        retry_delay_minutes=args.retry_delay_min,
        window_start_day=args.window_start_day,
        window_end_day=args.window_end_day,
    )
    sys.exit(code)
