import os
import datetime
import pandas as pd
import io
from ftplib import FTP
from dotenv import load_dotenv


load_dotenv(override=True)

class ADPConnect:
    def __init__(self):
        """
        Python class for downloading the latest time sheets for all employee hours
        into a byteArray from ADP FTP files connection.
        IBM Sterling sFTP service
        """
        self._user = os.getenv("JTS_FTP_USER")
        self._passwd = os.getenv("JTS_FTP_PASSWD")
        self._host = os.getenv("JTS_FTP_HOST")
    
    def formatted_date(self) -> str:
        """
        Method to format the date in `mmddyy` syntax which is included in the ADP hours CSV filename
        """
        now_date = datetime.datetime.now()
        formatted_now = str(now_date.strftime("%m-%d-%y"))
        formatted_now1 = formatted_now.replace("-","").replace(":","").replace(" ","")
        #formatted_now1 = "071724"
        return formatted_now1
    
    def listFileDir(self) -> list:
        with FTP() as ftp:
            try:
                ftp.connect(host=self._host, port=21)
                ftp.login(user=self._user, passwd=self._passwd)
                ftp.cwd('/OUTBOUND')
                files_dir = ftp.nlst()
                ftp.quit()
                return files_dir        
            except:
                print("Error retreiving list of files")
    
    def downloadFile(self, filename: str):
        with FTP() as ftp:
            try:
                ftp.connect(host=self._host, port=21)
                ftp.login(user=self._user, passwd=self._passwd)
                print("ADp FTP now connnected, you good to perform file operations.")
                ftp.cwd('/OUTBOUND')
                file_stream = io.BytesIO()
                ftp.retrbinary(f'RETR {filename}', file_stream.write)
                file_stream.seek(0)
                pandas_timereport_df = pd.read_csv(file_stream, header=0)
                ftp.quit()
                return pandas_timereport_df
            except:
                print("Error downloading list of files.")
                