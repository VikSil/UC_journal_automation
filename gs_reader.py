import pandas as pd 
from datetime import datetime
import argparse
from pathlib import Path
from environ import Env

def sheet_reader():
    """
    Google sheet reader based on argparse cprocessed command line arguements.

    This function uses argparse to process cli arguments to import google sheet data to csv for processing
    in selenium automation task but for data after a specific date.

    returns: pandas dataframe
    """

    BASE_DIR = Path(__file__).resolve().parent
    env = Env()
    env.read_env(BASE_DIR / 'credentials.env')

    # Get google sheet values from credentials
    GS_SHEET_ID = env("GS_SHEET_ID")
    

    # Initialize the parser
    parser = argparse.ArgumentParser(description="Filter CSV rows based on a date threshold.")

    # Add the threshold date argument
    parser.add_argument("threshold_date", type=str, help="Threshold date in M/D/YYYY format.")
    # Parse the arguments
    args = parser.parse_args()
    
    # Convert the provided threshold date string into a datetime object
    threshold_date = datetime.strptime(args.threshold_date, "%m/%d/%Y")
    # Custom date parser to match 'M/D/YYYY' format
    date_parser = lambda x: datetime.strptime(x, "%m/%d/%Y")

    df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{GS_SHEET_ID}/export?format=csv", parse_dates=["APPLICATION DATE"], date_parser=date_parser)
    
    df = df[df["APPLICATION DATE"] > threshold_date]
    df["APPLICATION DATE"] = df["APPLICATION DATE"].astype(str)
    return df

    
print(sheet_reader().iloc[:,3])
