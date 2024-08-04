import logging
import azure.functions as func
import azurestoragejts
import adpftp

app = func.FunctionApp()

@app.schedule(schedule="0 30 20 * * 1-5", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def timer_trigger_adpftp(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')

    adp = azurestoragejts.ADPConnect()
    date_now = adp.formatted_date()
    dir_files = adp.listFileDir()

    for filename in dir_files:
        print(filename)
        if (date_now in filename) and ("TimeandAttendancebyJobCostReport" in filename):
            jts = adpftp.JTSDatalake()

            fileStream = adp.downloadFile(filename)
            mimeType = filename.split(".")
            fileStreamName = f"adp-hours-archive/2024/adp-hours-{date_now}.{mimeType[-1]}"

            jts.uploadFileBlob(fileStream, fileStreamName, isPath=False)

            fileStreamName = f"adp-hours.{mimeType[-1]}"

            jts.uploadFileBlob(fileStream, fileStreamName, isPath=False)
            #spark_adphours_df = spark.createDataFrame(timereport_df)
        
        elif (date_now in filename) and ("ManagertoStaffRelationship" in filename):
            jts = adpftp.JTSDatalake()

            fileStream = adp.downloadFile(filename)
            mimeType = filename.split(".")
            fileStreamName = f"adp-org-archive/2024/adp-org-{date_now}.{mimeType[-1]}"

            jts.uploadFileBlob(fileStream, fileStreamName, isPath=False)

            fileStreamName = f"adp-org.{mimeType[-1]}"

            jts.uploadFileBlob(fileStream, fileStreamName, isPath=False)
            #spark_adporg_df = spark.createDataFrame(orgreport_df)