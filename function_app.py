import logging
import azure.functions as func
from resources import adpftp_jts, azureblob_jts
import pandas as pd
from io import StringIO

app = func.FunctionApp()

@app.schedule(schedule="0 30 16 * * 1-5", arg_name="myTimer", run_on_startup=True,
              use_monitor=False)  
def timer_trigger_ADPHours(myTimer: func.TimerRequest) -> None:
    """
    This time trigger Azure Function will run at 4:30pm EST every weekday to sync hours from ADP ftp to Blob Storage then update table in SQL
    Azure SQL Database: "dbo.SPAppCatalogArchive"   Table (dbo.ADPHours)
    Axure Blob Storage Container: "adp-hours"    Blob (TimeandReportingHours1.yymmddhhmmss.csv)
    """
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')

    adp = adpftp_jts.ADPConnect()

    date_now = adp.formatted_date()

    dir_files = adp.listFileDir()

    print(date_now)

    timereport_df = pd.DataFrame()

    for x in dir_files:
        print(x)
        if (date_now in x) and ("TimeandAttendancebyJobCostReport1" in x):
            print(x)
            timereport_df = adp.downloadFile(x)

            jts = azureblob_jts.JTSDatalake()

            # Send dataframe to stringify byte array for 
            csvFileBuffer = StringIO()
            csvFileName = f"adp-hours-archive/adp-hours-{date_now}.csv"

            timereport_df.to_csv(csvFileBuffer, index=False)

            jts.uploadCSVBlob(csvFileBuffer, csvFileName, isPath=False)

            # Write the base blob for the SQL virtual table into Azure Blob Storage
            csvFileName = "adp-hours.csv"

            jts.uploadCSVBlob(csvFileBuffer, csvFileName, isPath=False)