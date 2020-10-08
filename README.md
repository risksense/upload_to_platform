# Risksense - Upload to Platform

[Download version 1.1.2](https://github.com/risksense/upload_to_platform/releases/download/v1.1.2/upload_to_platform-v1.1.2.zip)

## Requirements

 - Python 3
    - This script has been tested using Python 3.7
 - Python Modules (recommend to install using pip):
    - toml
    - urllib3
    - requests
    - progressbar2
   
   `pip install -r requirements.txt`

## Overview
This Python script enables the upload of scan files to the RiskSense platform via the RiskSense API.

When run, the script will take all files from a designated folder, upload them to the RiskSense 
platform, and begin processing of those files.  Once the files have been successfully uploaded, 
the files will be moved into an "archive" subfolder within the original folder.


## Usage

##### Editing the configuration file (conf/config.toml):
 - Update the platform field as necessary.  
 - Add your API token.  
 - If it is known, you can provide the ID of the desired network (not the network name), and the user 
   will not be prompted to provide or find it.
 - Additionally, if the desired Client ID is known, you can provide it in the config file, and the 
   script will not ask the user about it.
 - If desired, change the paths of the folders containing the files to process and log file.
   - If you specify a custom path_to_files, ___be sure to create a subfolder named "archive" 
     within the folder specified___.

```toml
platform = 'https://platform.risksense.com'

# The API Token can be generated in the RiskSense UI, under User Settings.
api-key = ''

# Specify the path to the folder containing the files you wish to upload.
# If you update this, please use the absolute path to your desired folder.
files_folder = 'files_to_process'

# Specify the path to the folder you would like to use for logging.
# If you update this, please use the absolute path to your desired folder.
log_folder = 'logs'

# Trigger URBA upon completion of upload processing.
auto_urba = true

# You may uncomment this parameter and enter the desired network ID for your upload here if you already know it.
#network_id =

# You may uncomment this parameter and enter the desired client ID for your upload here if you already know it.
#client_id =

use_proxy = false

[proxy]
    host = ''
    port = 3128
    authentication = false
    user = ''
    password = ''

```


##### Running upload_to_platform.py:

After configuring the script, it can be executed as follows:
```commandline
python upload_to_platform.py
```

##### Advanced Usage
Any of the settings found in the configuration file can be overridden through the use of arguments 
at the time of execution.
```commandline

python upload_to_platform.py -h



         *** RiskSense -- upload_to_platform_v1.1.2 ***
Upload scan files to the RiskSense platform via the RiskSense API.
------------------------------------------------------------------

usage: upload_to_platform.py [-h] [-p PLATFORM] [-a API_KEY] [-f FILES_FOLDER]
                             [-l LOG_FOLDER] [-u {true,false}] [-c CLIENT_ID]
                             [-n NETWORK_ID] [--use_proxy USE_PROXY]
                             [--proxy_host PROXY_HOST]
                             [--proxy_port PROXY_PORT]
                             [--proxy_auth PROXY_AUTH]
                             [--proxy_user PROXY_USER] [--proxy_pwd PROXY_PWD]

The following arguments can be used to override those in the config file:

optional arguments:
  -h, --help                                    show this help message and
                                                exit
  -p PLATFORM, --platform PLATFORM              Platform URL
  -a API_KEY, --api_key API_KEY                 API Key
  -f FILES_FOLDER, --files_folder FILES_FOLDER  Path to folder containing scan
                                                files
  -l LOG_FOLDER, --log_folder LOG_FOLDER        Path to folder to write log
  -u {true,false}, --auto_urba {true,false}     Run auto-URBA?
  -c CLIENT_ID, --client_id CLIENT_ID           Client ID
  -n NETWORK_ID, --network_id NETWORK_ID        Network ID
  --use_proxy USE_PROXY                         Use Proxy?
  --proxy_host PROXY_HOST                       Proxy host
  --proxy_port PROXY_PORT                       Proxy port
  --proxy_auth PROXY_AUTH                       Use proxy authentication?
  --proxy_user PROXY_USER                       Proxy username
  --proxy_pwd PROXY_PWD                         Proxy password

```

Example -- overriding the network ID and scan file folder found in the config
```commandline
python upload_to_platform.py -n 12345 -f /home/johndoe/nessus_files
```
