#!/usr/bin/env python3
"""
whoop_pull.py — Export YOUR OWN per-minute heart-rate data from Whoop.

This is the same technique behind the "per-minute HR for the whole last week"
story: it uses the unofficial `whoop-data` client, which logs into the Whoop
*app's* internal API (not the limited official dev API) using YOUR credentials
and returns YOUR data only.

Setup:
    pip install whoop-data pandas
    export WHOOP_EMAIL="you@example.com"
    export WHOOP_PASSWORD="..."        # your own Whoop password

Run:
    python whoop_pull.py                       # last 7 days, your account
    python whoop_pull.py --label alice         # tag the output (for comparisons)
    python whoop_pull.py --days 14 --step 60   # custom window / interval

Output:
    whoop_hr_<label>.csv  with columns: timestamp, heart_rate
"""

import argparse
import getpass
import os
import sys
from datetime import date, timedelta

try:
    import pandas as pd
    from whoop_data import WhoopClient, get_heart_rate_data
except ImportError:
    sys.exit("Missing deps. Run: pip install whoop-data pandas")


def pull(email: str, password: str, days: int, step: int) -> "pd.DataFrame":
    """Authenticate as yourself and pull per-`step`-second HR for the last `days`."""
    end = date.today()
    start = end - timedelta(days=days)

    try:
        client = WhoopClient(username=email, password=password)
    except Exception as e:
        raise SystemExit(
            f"\nWhoop login was rejected ({e}).\n"
            "The script and request format are correct — Whoop refused these credentials.\n"
            "Most likely cause, in order:\n"
            "  1. Your Whoop account uses 'Continue with Google/Apple' (SSO). Such accounts\n"
            "     have NO password this login endpoint accepts. Fix: in the Whoop app go to\n"
            "     Settings > Account and set an email+password login, then use those here.\n"
            "  2. Wrong password, or special characters mangled by the shell. Re-export with\n"
            "     single quotes:  export WHOOP_PASSWORD='your#real$pass'\n"
            "  3. Two-factor auth is enabled — this unofficial endpoint can't pass 2FA.\n"
        )
    # Whoop's HR endpoint rejects any request spanning more than 168 hours, and
    # the library bumps the end date to 23:59:59, so even a 7-day range becomes
    # ~191h. Fetch one day at a time and concatenate — well under the cap.
    raw = []
    day = start
    while day < end:
        chunk = get_heart_rate_data(
            client=client,
            start_date=day.isoformat(),
            end_date=day.isoformat(),  # single calendar day (~24h window)
            step=step,  # 60 = one sample per minute (also supports 6 and 600)
        )
        print(f"  {day.isoformat()}: {len(chunk):,} samples")
        raw.extend(chunk)
        day += timedelta(days=1)

    # whoop-data returns dicts shaped like:
    #   {"timestamp": <unix_ms>, "datetime": "2023-..Z", "heart_rate": <bpm>}
    # NOTE: "timestamp" is Unix milliseconds, NOT a date string — parse with unit="ms".
    df = pd.DataFrame(raw)
    if df.empty:
        return df
    df = df.drop_duplicates(subset="timestamp")  # guard against day-boundary overlap
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df[["timestamp", "heart_rate"]].sort_values("timestamp").reset_index(drop=True)
    return df


def main() -> None:
    ap = argparse.ArgumentParser(description="Export your per-minute Whoop heart rate.")
    ap.add_argument("--label", default="me", help="tag for the output file (e.g. your name)")
    ap.add_argument("--days", type=int, default=7, help="how many days back (default 7)")
    ap.add_argument("--step", type=int, default=60, help="seconds per sample (60 = per-minute)")
    args = ap.parse_args()

    # Use env vars if set (handy for the analyst); otherwise just ask. Prompting
    # avoids all the shell-quoting pain with passwords containing ! $ " etc.
    email = os.environ.get("WHOOP_EMAIL")
    password = os.environ.get("WHOOP_PASSWORD")
    if not email:
        email = input("Whoop email: ").strip()
    if not password:
        password = getpass.getpass("Whoop password (hidden as you type): ")
    if not email or not password:
        sys.exit("Email and password are required.")

    df = pull(email, password, args.days, args.step)
    if df.empty:
        sys.exit("No heart-rate data returned for that window.")

    out = f"whoop_hr_{args.label}.csv"
    df.to_csv(out, index=False)
    print(f"Saved {len(df):,} samples ({args.days}d @ {args.step}s) -> {out}")
    print(df.head())


if __name__ == "__main__":
    main()
