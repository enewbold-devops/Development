import os
import logging
import json
import azure.functions as func
from azure.functions.decorators.core import DataType
from datetime import datetime, date, timedelta
import azurestoragejts
import adpftp
import payperiod as pp
import pandas as pd


payperiod_dates = pp.currentPayperiod()

app = func.FunctionApp()

##############################    ADP FTP Extract Function    #########################################

@app.schedule(schedule="0 30 20 * * 1-5", arg_name="myADPTimer", run_on_startup=False,
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
    jts = azurestoragejts.JTSDatalake()

    date_now = adp.formatted_date()
    dir_files = adp.listFileDir()

    reportlist = [
        {
            "reporttype": "TimeandAttendanceByJobCostReport1",
            "blobprefix": "adp-hours"
        },
        {
            "reporttype": "ManagertoStaffRelationship",
            "blobprefix": "adp-org"
        }
    ]

    print(dir_files)
    
    for report in reportlist:
        for filename in dir_files:

            report_type= report["reporttype"]
            blobprefix = report["blobprefix"]

            if (date_now in filename) and (report_type in filename):

                fileStream = adp.downloadFile(filename)
                mimeType = filename.split(".")

                fileStreamName = f"{blobprefix}-archive/{datetime.now().year}/{blobprefix}-{date_now}.{mimeType[-1]}"
                jts.uploadFileBlob(fileStream, fileStreamName, isPath=False)

                fileStreamName = f"{blobprefix}.{mimeType[-1]}"
                jts.uploadFileBlob(fileStream, fileStreamName, isPath=False)



##############################    SQL PayPerion Hours Insert Function      #########################################


@app.function_name(name="timer_trigger_adpsql")
@app.schedule(schedule="0 0 21 * * 1-5", arg_name="mySQLTimer", run_on_startup=False,
              use_monitor=False)
@app.sql_input(arg_name="SQLProcedureRemoveADPHrs",
               command_text="[dbo].[RemoveADPCurrentPayperiodHours]",
               command_type="StoredProcedure",
               parameters=f"@StartDate={payperiod_dates[0]},@EndDate={payperiod_dates[1]}",
               connection_string_setting="AZURE_SQL_CONNECT_STRING"
               )
@app.sql_output(arg_name="SQLHoursArchive",
                command_text="[dbo].[ADPHoursArchive]",
                connection_string_setting="AZURE_SQL_CONNECT_STRING")
def timer_trigger_adpsql(mySQLTimer: func.TimerRequest, SQLProcedureRemoveADPHrs: func.SqlRowList, SQLHoursArchive: func.Out[func.SqlRow]) -> None:
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

    payperiod_hours_df = pd.DataFrame()

    start_date = datetime.strptime(payperiod_dates[0],"%Y-%m-%d")
    end_date = datetime.strptime(payperiod_dates[1],"%Y-%m-%d")

    if start_date <= datetime.now() <= end_date:

        resp = list(map(lambda r: json.loads(r.to_json()), SQLProcedureRemoveADPHrs))

        #print("Replaced rows for payperiod =>." + json.dump(resp))

        timereport_df = jts.downloadADPBlob("hours") #get the current adp-hours.csv into a dataframe
        timereport_df['Date'] = pd.to_datetime(timereport_df['Date'], format='%m/%d/%Y')
        payperiod_hours_df =  timereport_df[(timereport_df['Date'] >= start_date) & (timereport_df['Date'] <= end_date)]
        payperiod_hours_df["Sub-Project"].fillna("None", inplace=True)
        payperiod_hours_df["Date"] = payperiod_hours_df["Date"].astype(str)
        payperiod_hours_df.rename(columns={"Sub-Project":"Sub_Project", "ID Number": "ID_Number"}, inplace=True)

        adphours_load =  payperiod_hours_df.to_json(orient="records", indent=4)

        adphours_list = json.loads(adphours_load)

        rows = func.SqlRowList(map(lambda row: func.SqlRow.from_dict(row), adphours_list))

        SQLHoursArchive.set(rows)