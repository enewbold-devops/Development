import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv


load_dotenv()

# Acquire a credential object
# https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication-local-development-service-principal?tabs=azure-cli
# https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-directory-file-acl-python?tabs=azure-ad

class JTSDatalake:
    def __init__(self):
        self._blobacct = "enewboldpowerbi"
        self._blobcont = "adp-hours"
        self._accesskey = os.getenv("AZURE_BLOB_ACCESSKEY")
        self._connect_string = f"DefaultEndpointsProtocol=https;AccountName={self._blobacct};AccountKey={self._accesskey};EndpointSuffix=core.windows.net"

    def uploadCSVBlob(self, fileblob, fileblobname, isPath: bool):
        account_url = f"https://{self._blobacct}.blob.core.windows.net"

        blob_service_client = BlobServiceClient(account_url, credential=self._accesskey)

        if isPath:
            blob_client = blob_service_client.get_blob_client(container=self._blobcont, blob=fileblob)
            with open(file=fileblob, mode="rb") as data:
                blob_client.upload_blob(data, blob_type="BlockBlob", overwrite=True)
        else:  
            container_client = blob_service_client.get_container_client(self._blobcont)
            blob_client = container_client.get_blob_client(fileblobname)
            blob_client.upload_blob(fileblob.getvalue(), blob_type="BlockBlob", overwrite=True)

"""
class JTSAzureSQL:
    def __init__(self):
        self._conn_string = ""
"""