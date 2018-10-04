# Risksense - Upload to Platform

## Requirements

 - Python 3
    - This script has been tested using Python 3.7
 - Python Modules (recommend to install using pip):
    - toml
      - `pip install toml`
    - requests
      - `pip install requests`
    
## Overview
This Python script enables the upload of scan files to the Risksense platform via the REST API.

When run, the script will take all files from a designated folder, upload them to the Risksense platform, and begin processing of those files.  Once the files have been successfully uploaded, the files will be moved into an "archive" subfolder within the original folder.

The script does not currently support multi-client users.  If the user associated with the specified API key is a multi-client user, it will default to the first client ID returned in the list from the REST API.    


## Basic Usage

##### Editing the configuration file:
 - Update the platform field as necessary.  
 - Add your API token.  
 - If it is known, you can provide the ID of the desired network (not the network name), and the user will not be prompted to provide or find it.
 - If desired, change the paths of the folders containing the files to process and log file.
   - If you specify a custom path_to_files, be sure to create a subfolder named "archive" within the folder specified.

```
platform = "https://platform.risksense.com"

# The API Token can be generated in the RiskSense UI, under User Settings.
api-key = ""

# You may uncomment this parameter and enter the desired network ID for your upload here if you already know it.
network_id = ""

# Specify the path to the folder containing the files you wish to upload
path_to_files = "files_to_process"

# Specify the path to the folder you would like to use for logging.
path_to_logs = "logs"
```


##### Running upload_to_platform.py:
```
 $ python upload_to_platform.py
```