import os
import datetime
import pandas as pd
import io
from ftplib import FTP
from dotenv import load_dotenv

load_dotenv()

class ADPConnect:
    def __init__(self):
        """
        Class for downloading the latest time sheets for all employee hours
        into a byteArray from ADP FTP files connection.
        IBM Sterling sFTP service
        """
        self._user = os.getenv("JTS_FTP_USER")
        self._passwd = os.getenv("JTS_FTP_PASSWD")
        self._host = os.getenv("JTS_FTP_HOST")
    
    def formatted_date(self) -> str:
        """
        Method to format the date in `mmddyy` syntax which is included in the ADP hours CSV filename
        returns @str
        """
        now_date = datetime.datetime.now()
        formatted_now = str(now_date.strftime("%m-%d-%y"))
        #formatted_now1 = formatted_now.replace("-","").replace(":","").replace(" ","")
        formatted_now1 = "072624"
        return formatted_now1
    
    def listFileDir(self) -> list:
        """
        Method to connect to the FTP at ADP then return the list of files in a directory
        returns type @list
        """
        with FTP() as ftp:
            try:
                ftp.connect(host=self._host, port=21)
                ftp.login(user=self._user, passwd=self._passwd)
                ftp.cwd("/OUTBOUND")
                files_dir = ftp.nlst()
                ftp.quit()
                return files_dir        
            except:
                print("Error retreiving list of files")
    
    def downloadFile(self, filename) -> io.BytesIO:
        """
        Method to connect to the FTP at ADP then return a binary filestream on the 
        terminal shell command retrieve file "RETR <filename>"
        returns type @io.BytesIO
        """
        with FTP() as ftp:
            try:
                ftp.connect(host=self._host, port=21)
                ftp.login(user=self._user, passwd=self._passwd)
                print("FTP is now connnected...")
                ftp.cwd('/OUTBOUND')
                file_stream = io.BytesIO()
                ftp.retrbinary(f"RETR {filename}", file_stream.write)
                file_stream.seek(0)
                ftp.quit()
                return file_stream
            except:
                print("FTP not connect so file is not downloaded as ByteIO Stream.")
                