# Introduction 
Azure Functions project to process ADP data 
* ADP Hours data
* Import client, project and sub-projects 

# Getting Started
## Pre-requisites
* Python 3.11 or above
* Visual Studio Code or your favorite IDE

## Build
* Checkout latest code (which you already have if you are reading this README)
* Open a command prompt and change to directory where you have checkout the code
* Create a virtual environment and activate the virtual env.<br>(Type following commands in command prompt)

    ```
    python -m venv .venv
    .\.venv\Source\activate
    ```
* Use the virtual environment during all your development and testing
* Install required dependencies from the same command prompt
    ```
    pip install -r requirements.txt
    ```

## Local Development
Create a "local.settings.json" file at root level of project with following JSON content. 

Replace placeholder values (with <> brackets) with actual for your local testing. <b>NEVER USE PRODUCTION VALUES FOR TESTING.</b>    

    {
        "IsEncrypted": false,
        "Values": {
            "FUNCTIONS_WORKER_RUNTIME": "python",
            "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
            "AzureWebJobsStorage": "UseDevelopmentStorage=true",
            "DBURL": "DRIVER={SQL Server};SERVER=<DBSERVER>;DATABASE=<DBNAME>;UID=<DBUSER>;PWD=<DBPASS>",
            "JTS_FTP_HOST": "<FTP_HOST>",
            "JTS_FTP_USER": "<FTP_USER>",
            "JTS_FTP_PASSWD": "<FTP_PASS>",
            "ADP_HOURS_FILE_NAME": "adp-hours.csv",
            "ADP_PAYROLL_DAY_CNT": 14,
            "AZURE_STORAGE_ACCT": "http://127.0.0.1:10000/devstoreaccount1",
            "AZURE_BLOB_ACCESSKEY": "Enter SAS Token Here",
            "AZURE_BLOB_CONTAINER": "adphours-upload",
            "AZURE_SQL_CONNECT_STRING": "DRIVER={SQL Server};SERVER=<DBSERVER>;DATABASE=<DBNAME>;UID=<DBUSER>;PWD=<DBPASS>"
        }
    }

# Contribute
* Create a new branch from the `development` branch
    ```
    git checkout development
    git pull
    git checkout -b "New_branch_Name"
    ```
* Develop and checkin all changes in the new branch and push it to server
* Create a new pull request to merge in "develop-pure" branch
* As final deployment we collect all changes from develop branch and create a new pull request to merge to main, which will kick off automated CI/CD pipeline to deploy to PRODUCTION Azure Functions
