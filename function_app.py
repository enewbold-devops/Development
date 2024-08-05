import os
import logging
import json
import azure.functions as func
from azure.functions.decorators.core import DataType
from datetime import datetime, date, timedelta
import azurestoragejts
import adpftp
import pandas as pd

app = func.FunctionApp()

##############################    ADP FTP Extract Function    #########################################

@app.schedule(schedule="0 30 20 * * 1-5", arg_name="myADPTimer", run_on_startup=True,
              use_monitor=False) 
def timer_trigger_adpftp(myADPTimer: func.TimerRequest) -> None:
    """
    Azure Function: timer trigger running every weekeday at 8:30PM EAST-US
    This process reads adp hours, organzation csb file from the ADP FTP Server (IBM Sterling)
    then syncs the file into the business Azure Blob storage container "adp-hours"
    """
    if myADPTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')

    adp = adpftp.ADPConnect()
    date_now = adp.formatted_date()
    dir_files = adp.listFileDir()

    for filename in dir_files:
        print(filename)
        if (date_now in filename) and ("TimeandAttendancebyJobCostReport1" in filename):

            jts = azurestoragejts.JTSDatalake()

            fileStream = adp.downloadFile(filename)
            mimeType = filename.split(".")
            fileStreamName = f"adp-hours-archive/{datetime.now().year}/adp-hours-{date_now}.{mimeType[-1]}"

            jts.uploadFileBlob(fileStream, fileStreamName, isPath=False)

            fileStreamName = f"adp-hours.{mimeType[-1]}"

            jts.uploadFileBlob(fileStream, fileStreamName, isPath=False)
            #spark_adphours_df = spark.createDataFrame(timereport_df)
        
        elif (date_now in filename) and ("ManagertoStaffRelationship" in filename):

            jts = azurestoragejts.JTSDatalake()

            fileStream = adp.downloadFile(filename)
            mimeType = filename.split(".")
            fileStreamName = f"adp-org-archive/{datetime.now().year}/adp-org-{date_now}.{mimeType[-1]}"

            jts.uploadFileBlob(fileStream, fileStreamName, isPath=False)

            fileStreamName = f"adp-org.{mimeType[-1]}"

            jts.uploadFileBlob(fileStream, fileStreamName, isPath=False)
            #spark_adporg_df = spark.createDataFrame(orgreport_df)



##############################    SQL Insert Function      #########################################

@app.function_name(name="timer_trigger_adpsql")
@app.schedule(schedule="0 0 21 * * 1-5", arg_name="mySQLTimer", run_on_startup=True,
              use_monitor=False)
@app.sql_output(arg_name="SQLHoursArchive",
                command_text="[dbo].[ADPHoursArchive]",
                connection_string_setting="AZURE_SQL_CONNECT_STRING")
def timer_trigger_adpsql(mySQLTimer: func.TimerRequest, SQLHoursArchive: func.Out[func.SqlRowList]) -> None:
    """
    Azure Function: timer trigger running every weekeday at 9:00PM EAST-US
    1) This process reads adp hours from the business Azure Blob storage container "adp-hours".
    2) Next, it compares the current date in the current payroll schedule week.
    3) Lastly, its reads from the latest adp-hours ftp dump and gets the hours for the current payperiod
    and appends the records to the SQL table replacing the hours for the current payperiod
    """
    if mySQLTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')

    jts = azurestoragejts.JTSDatalake()

    # Get current payroll schedule
    payroll_df = jts.downloadADPBlob("payrollschedule") 

    payperiod_hours_df = pd.DataFrame()

    for period_end in payroll_df["Period End"]:

        # Evaluate start & end of the current payperiod
        payroll_end_date = datetime.strptime(period_end, "%m/%d/%Y")
        payroll_start_date = payroll_end_date - timedelta(days= int(os.getenv("ADP_PAYROLL_DAY_CNT"))) 

        # Check if current date is within the current payperiod
        is_between = payroll_start_date <= datetime.now() <= payroll_end_date

        if is_between:
            timereport_df = jts.downloadADPBlob("hours") #get the current adp-hours.csv into a dataframe
            timereport_df['Date'] = pd.to_datetime(timereport_df['Date'], format='%m/%d/%Y')
            payperiod_hours_df =  timereport_df[(timereport_df['Date'] >= payroll_start_date) & (timereport_df['Date'] <= payroll_end_date)]

            payperiod_hours_df.drop(columns=["Employment Profile - Effective Date"], inplace=True)
            payperiod_hours_df["Sub-Project"].fillna("None", inplace=True)
            payperiod_hours_df["Date"] = payperiod_hours_df["Date"].astype(str)
            payperiod_hours_df.rename(columns={"Sub-Project":"Sub_Project", "ID Number": "ID_Number"}, inplace=True)

            adphours_load =  payperiod_hours_df.to_json(orient="records", indent=4)

            rows = func.SqlRowList(map(lambda row: func.SqlRow.from_dict(row), adphours_load))

            SQLHoursArchive.set(rows)