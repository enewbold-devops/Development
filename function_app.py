import logging
import azure.functions as func
import azurestoragejts
import adpftp

app = func.FunctionApp()

@app.schedule(schedule="0 30 20 * * 1-5", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def timer_trigger_adpftp(myTimer: func.TimerRequest) -> None:
    """
    Azure Function: timer trigger running every weekeday at 8:30PM EAST-US
    This process reads adp hours, organzation csb file from the ADP FTP Server (IBM Sterling)
    then syncs the file into the business Azure Blob storage container "adp-hours"
    """
    if myTimer.past_due:
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
            fileStreamName = f"adp-hours-archive/2024/adp-hours-{date_now}.{mimeType[-1]}"

            jts.uploadFileBlob(fileStream, fileStreamName, isPath=False)

            fileStreamName = f"adp-hours.{mimeType[-1]}"

            jts.uploadFileBlob(fileStream, fileStreamName, isPath=False)
            #spark_adphours_df = spark.createDataFrame(timereport_df)
        
        elif (date_now in filename) and ("ManagertoStaffRelationship" in filename):

            jts = azurestoragejts.JTSDatalake()

            fileStream = adp.downloadFile(filename)
            mimeType = filename.split(".")
            fileStreamName = f"adp-org-archive/2024/adp-org-{date_now}.{mimeType[-1]}"

            jts.uploadFileBlob(fileStream, fileStreamName, isPath=False)

            fileStreamName = f"adp-org.{mimeType[-1]}"

            jts.uploadFileBlob(fileStream, fileStreamName, isPath=False)
            #spark_adporg_df = spark.createDataFrame(orgreport_df)


@app.schedule(schedule="0 0 21 * * 1-5", arg_name="mySQLTimer", run_on_startup=True,
              use_monitor=False)
def timer_trigger_adpsql(mySQLTimer: func.TimerRequest) -> None:
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
