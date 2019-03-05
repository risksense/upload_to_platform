# Risksense - Upload to Platform
[Download version 0.3](https://github.com/risksense/upload_to_platform/releases/download/v0.3/upload_to_platform.zip)

## Requirements

 - Python 3
    - This script has been tested using Python 3.7
 - Python Modules (recommend to install using pip):
    - toml
    - requests
    - progressbar2
   
   `pip install -r requirements.txt`

## Overview
This Python script enables the upload of scan files to the Risksense platform via the REST API.

When run, the script will take all files from a designated folder, upload them to the Risksense platform, and begin processing of those files.  Once the files have been successfully uploaded, the files will be moved into an "archive" subfolder within the original folder.



## Basic Usage

##### Editing the configuration file:
 - Update the platform field as necessary.  
 - Add your API token.  
 - If it is known, you can provide the ID of the desired network (not the network name), and the user will not be prompted to provide or find it.
 - Additionally, if the desired Client ID is known, you can provide it in the config file, and the script will not ask the user about it.
 - If desired, change the paths of the folders containing the files to process and log file.
   - If you specify a custom path_to_files, be sure to create a subfolder named "archive" within the folder specified.

```
platform = 'https://platform.risksense.com'

# The API Token can be generated in the RiskSense UI, under User Settings.
api-key = ''

# Specify the path to the folder containing the files you wish to upload.
# If you update this, please use the absolute path to your desired folder.
files_folder = 'files_to_process'

# Specify the path to the folder you would like to use for logging.
# If you update this, please use the absolute path to your desired folder.
log_folder = 'logs'

# You may uncomment this parameter and enter the desired network ID for your upload here if you already know it.
#network_id =

# You may uncomment this parameter and enter the desired client ID for your upload here if you already know it.
#client_id =
```


##### Running upload_to_platform.py:
```
 $ python upload_to_platform.py
```
