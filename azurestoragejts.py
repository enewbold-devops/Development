import os
import io
#from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
#from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv


load_dotenv()

# Acquire a credential object
# https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication-local-development-service-principal?tabs=azure-cli
# https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-directory-file-acl-python?tabs=azure-ad

class JTSDatalake:
    def __init__(self):
        self._blobacct = os.getenv("AZURE_STORAGE_ACCT")
        self._blobcont = os.getenv("AZURE_BLOB_CONTAINER")
        self._accesskey = os.getenv("AZURE_BLOB_ACCESSKEY")

    def downloadFileBlob(self, adpChoice, date, isArchive) -> io.StringIO:
        """
        Method for downlaoding a blob from the JTS ADP storage container
        @adpChoice = "hours" | "payschedule" | "org"
        @date = "mmddyy" #file archive date to return blob through a filestream if @isArchive = true
        @isArchive = true | false  #file blob from archive directory and @date to get daily archive dump

        """
        pass
        
    def uploadFileBlob(self, fileblob, fileblobname: str, isPath: bool):
        """
        Method for uploading a file blob to Azure storage container
        @fileblob = io.BytesIO | io.StringIO #filestream of the Blob
        @fileblobname = str #filename or filepath if @isPath = true
        @isPath = bool 
        """
        account_url = f"https://{self._blobacct}.blob.core.windows.net"

        blob_service_client = BlobServiceClient(account_url, credential=self._accesskey)

        if isPath:
            blob_client = blob_service_client.get_blob_client(container=self._blobcont)
            with open(file=fileblobname, mode="rb") as data:
                blob_client.upload_blob(data, blob_type="BlockBlob", overwrite=True)
        else:  
            container_client = blob_service_client.get_container_client(self._blobcont)
            blob_client = container_client.get_blob_client(fileblobname)
            blob_client.upload_blob(fileblob.getvalue(), blob_type="BlockBlob", overwrite=True)


"""class JTSAzureSQL:
    def __init__(self):
        self._conn = {
            "database_type":"mssql+pyodbc",
            "driver": "ODBC Driver 17 for SQL Server",
            "server": os.getenv("AZURE_SQL"),
            "user": os.getenv("AZURE_SQL_LOGIN"),
            "password": os.getenv("AZURE_SQL_PASSWD"),
            "database": 'SPAppCatalogArchive'
        }
        self._table = "ADPHoursArchive"
        
    def execQuery(self, df):
        
        engine = create_engine(
            f"{self._conn.database_type}://{self._conn.user}:{self._conn.password}@{self._conn.server}/{self._conn.database}?driver={self._conn.driver}"
        )

        with engine.connect() as azsql:
            try:
                df.to_sql(self._table, engine, if_exists='append', index=False)
                print(f"ADP hours inserted suscessfully in dbo.{self._table}")

                result = azsql.execute(f"SELECT Count(*) FROM dbo.{self._table} Where CreatedOn = getdate()")
                for row in result:
                    print(row)
            except:
                print("There was an error inserting the data")"""