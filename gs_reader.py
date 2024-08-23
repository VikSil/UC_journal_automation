import argparse
import pandas as pd
from datetime import datetime
from environ import Env
from pathlib import Path


def sheet_reader():
    """
    This function uses argparse to process cli arguments and imports google sheet data to csv for processing

    Argument (optional):
    -d --threshold-date : The earliest application date to be processed

    Surpassed by environment variable START_DATE
    If no value is available, all data since 1999-12-31 will be processed

    Function returns a Pandas Dataframe
    """

    BASE_DIR = Path(__file__).resolve().parent
    env = Env()
    env.read_env(BASE_DIR / 'credentials.env')

    # Get values from credentials
    GS_SHEET_ID = env("GS_SHEET_ID")
    DATE_FORMAT = env('DATE_FORMAT')

    if 'START_DATE' in env:
        threshold_date = env('START_DATE')
    else:
        # Initialize the parser
        parser = argparse.ArgumentParser(description="Filter CSV rows based on a date threshold.")

        # Add the threshold date argument
        parser.add_argument(
            "-d",
            "--threshold-date",
            type=str,
            help=f"Earliest application date in {DATE_FORMAT} format.",
            default=datetime.now().strftime(DATE_FORMAT),
        )
        # Parse the arguments
        args = parser.parse_args()

        # Convert the provided threshold date string into a datetime object
        threshold_date = datetime.strptime(args.threshold_date, DATE_FORMAT)

    df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{GS_SHEET_ID}/export?format=csv")
    df = df[df["APPLICATION DATE"].notna()]
    df["APPLICATION DATE"] = pd.to_datetime(df["APPLICATION DATE"], format=DATE_FORMAT)
    df = df[df["APPLICATION DATE"] >= threshold_date]
    df["APPLICATION DATE"] = df["APPLICATION DATE"].astype(str)
    df = df.query("STATUS in ('Applied', 'Unsuccessful')")

    return df
