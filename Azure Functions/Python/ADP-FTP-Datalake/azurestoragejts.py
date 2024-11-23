import os
import io
#from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient
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

    def downloadADPBlob(self, adpChoice: str) -> pd.DataFrame:
        """
        Method for downlaoding a blob from the JTS ADP storage container
        @adpChoice = "hours" | "payrollschedule" | "org"

        """
        account_url = self._blobacct
       

        blob_service_client = BlobServiceClient(account_url, credential=self._accesskey)

        if adpChoice == "hours":
            blob_client = blob_service_client.get_blob_client(container=self._blobcont, blob=f"adp-{adpChoice}.csv")
        elif adpChoice == "payrollschedule":
            blob_client = blob_service_client.get_blob_client(container=self._blobcont, blob=f"adp-{adpChoice}.csv")
        elif adpChoice == "org":
            blob_client = blob_service_client.get_blob_client(container=self._blobcont, blob=f"adp-{adpChoice}.csv")
        else:
            return pd.DataFrame() #blank dataframe
        
        blob_data = blob_client.download_blob().content_as_text()

        return pd.read_csv(io.StringIO(blob_data))
        
        
    def uploadFileBlob(self, fileblob, fileblobname: str, isPath: bool):
        """
        Method for uploading a file blob to Azure storage container
        @fileblob = io.BytesIO | io.StringIO #filestream of the Blob
        @fileblobname = str #filename or filepath if @isPath = true
        @isPath = bool 
        """
        #TODO: Set https://{self._blobacct}.blob.core.windows.net as environment value in Azure
        account_url = self._blobacct

        blob_service_client = BlobServiceClient(account_url, credential=self._accesskey)

        if isPath:
            blob_client = blob_service_client.get_blob_client(container=self._blobcont)
            with open(file=fileblobname, mode="rb") as data:
                blob_client.upload_blob(data, blob_type="BlockBlob", overwrite=True)
        else:  
            container_client = blob_service_client.get_container_client(self._blobcont)
            blob_client = container_client.get_blob_client(fileblobname)
            blob_client.upload_blob(fileblob.getvalue(), blob_type="BlockBlob", overwrite=True)
