import os
from datetime import datetime, date, timedelta
import azurestoragejts
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def currentPayperiod() -> list:
    """
    Function to return the payperiod for the current date
    """
    jts = azurestoragejts.JTSDatalake()
    #print("Downloading payrollschedule csv file from Azure Storage")
    payroll_df = jts.downloadADPBlob("payrollschedule") 

    for period_end in payroll_df["Period End"]:

        # Evaluate start & end of the current payperiod
        payroll_end_date = datetime.strptime(period_end, "%m/%d/%Y")
        payroll_start_date = payroll_end_date - timedelta(days= int(os.getenv("ADP_PAYROLL_DAY_CNT"))) 

        # Check if current date is within the current payperiod
        is_between = payroll_start_date <= datetime.now() <= payroll_end_date

        if is_between:
            start_date = str(payroll_start_date).split()[0]
            end_date = str(payroll_end_date).split()[0]
            print(f"Payroll Start Date =>  {start_date}")
            print(f"Payroll End Date =>  {end_date}")
            return [start_date, end_date]
