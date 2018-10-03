###################################################
#
#  Written By: Burr Webb
#  For RiskSense, Inc.
#  2018
#
###################################################

import json
import time
import datetime
import sys
import os
import logging
import toml
import shutil
import requests



#########################
#
#  Get Client ID
#
#########################
def get_client_id(platform, key):

    logging.info("Getting Client ID")
    url = platform + "/api/v1/client"
    header = {'x-api-key': key,
              'content-type': 'application\json'
              }

    raw_client_id_response = requests.get(url, headers=header)

    json_client_id_response = json.loads(raw_client_id_response.text)

    if raw_client_id_response.status_code == 200:
        found_id = json_client_id_response['_embedded']['clients'][0]['id']

    else:
        print(f"Error Getting Client ID: Status Code returned was {raw_client_id_response.status_code}")
        return

    return found_id


#########################
#
#  Find Network ID
#
#########################
def find_network_id(platform, key, client):

    logging.info("Getting Network ID")

    network_id_known = input("Do you know the network ID for your upload? (y/n) ")
    logging.info("Does customer know network ID? %s", network_id_known)

    if network_id_known.lower() == 'y':
        network = input("Input network ID: ")
        return network

    else:
        search_value = input("Input search string for Network name search (or hit 'ENTER' to list all): ")
        logging.info("Customer search string: %s", search_value)

        logging.info("Querying network IDs based on search string")
        url = platform + "/api/v1/client/" + str(client) + "/network/search"
        header = {'x-api-key': key,
                  'Content-Type': "application/json",
                  'Cache-Control': "no-cache"
                  }
        body = {"filters": [
            {
                "field": "name",
                "exclusive": False,
                "operator": "LIKE",
                "value": search_value
            }
        ],
            "projection": "basic",
            "sort": [
                {
                    "field": "id",
                    "direction": "ASC"
                }
            ],
            "page": 0,
            "size": 20
        }

        raw_network_search_response = requests.post(url, headers=header, data=json.dumps(body))
        json_network_search_response = json.loads(raw_network_search_response.text)

        if raw_network_search_response.status_code == 200:
            z = 0
            network_list = []
            while z < len(json_network_search_response['_embedded']['networks']):
                if json_network_search_response['_embedded']['networks'][z]['clientId'] == client:
                    network_list.append([json_network_search_response['_embedded']['networks'][z]['id'], json_network_search_response['_embedded']['networks'][z]['name']])
                z += 1

            y = 0
            while y < len(network_list):
                print(f"{y} - {network_list[y][1]}")
                y += 1

            list_id = input("Please enter the number that corresponds with your network: ")
            network = network_list[int(list_id)][0]

        else:
            print(f"An error occurred during the search for your network.  Status code returned was {raw_network_search_response.status_code}")
            return

    return network


##############################
#
#  Create a New Assessment
#
##############################

def create_new_assessment(platform, key, client, name, start_date, notes):

    logging.info("Creating new assessment.")
    logging.debug("New assessment name: %s", name)
    logging.debug("New assessment start date: %s", start_date)
    logging.debug("New assessment notes: %s", notes)

    url = platform + "/api/v1/client/" + str(client) + "/assessment"
    header = {'x-api-key': key,
              'Content-Type': "application/json",
              'Cache-Control': "no-cache"
              }
    body = {"name": name,
            "startDate": start_date,
            "notes": notes
            }

    raw_assessment_response = requests.post(url, headers=header, data=json.dumps(body))
    json_assessment_response = json.loads(raw_assessment_response.text)

    if raw_assessment_response.status_code == 201:
        created_id = json_assessment_response['id']
    else:
        print(f"Error Creating New Assessment.  Status Code returned was {raw_assessment_response.status_code}")
        return

    return created_id


##################################
#
#  Create Upload for Assessment
#
##################################
def create_upload(platform, key, assessment, network, client):

    logging.info("Creating new upload.")

    upload_name = "upload-" + str(today) + "-" + str(current_time)

    url = platform + "/api/v1/client/" + str(client) + "/upload"
    header = {'x-api-key': key,
              'Content-Type': "application/json",
              'Cache-Control': "no-cache"
              }
    body = {'assessmentId': assessment,
            'networkId': network,
            'name': upload_name
            }

    raw_upload_response = requests.post(url, headers=header, data=json.dumps(body))
    json_upload_json_response = json.loads(raw_upload_response.text)

    if raw_upload_response.status_code == 201:
        new_upload_id = json_upload_json_response['id']
    else:
        print(f"Error creating new upload.  Status Code returned was {raw_upload_response.status_code}")
        return

    return new_upload_id


#########################
#
#  Add File to Upload
#
#########################
def add_file_to_upload(platform, key, client, upload, file_name, file_path):

    logging.info("Adding file to upload: %s", file_name)
    logging.debug("File Path: %s", file_path)

    print(f"Uploading file - {file_name}...")

    url = platform + "/api/v1/client/" + str(client) + "/upload/" + str(upload) + "/file"
    header = {'x-api-key': key,
              'Cache-Control': "no-cache"
              }

    upload_file = {'scanFile': (file_name, open(file_path + "/" + file_name, 'rb'))}

    raw_add_file_response = requests.post(url, headers=header, files=upload_file)
    # json_add_file_response = json.loads(raw_add_file_response.text)

    if raw_add_file_response.status_code != 201:
        print(f"Error uploading file {file_name}.  Status Code returned was {raw_add_file_response.status_code}")


##############################
#
#  Start Processing Upload
#
##############################
def begin_processing(platform, key, client, upload):

    logging.info("Starting platform processing")

    url = platform + "/api/v1/client/" + str(client) + "/upload/" + str(upload) + "/start"
    header = {'x-api-key': key,
              'Content-Type': "application/json",
              'Cache-Control': "no-cache"
              }

    raw_begin_processing_response = requests.post(url, headers=header)

    if raw_begin_processing_response.status_code == 204:
        print("Uploaded file(s) now processing.  This may take a while. Please wait...")
        return
    else:
        print("An error has occurred when trying to start processing of your upload(s).")
        return


############################################################
#
#  Check Status of Upload
#
############################################################
def check_upload_state(platform, key, client, upload):

    logging.info("Checking status of the upload processing")

    url = platform + "/api/v1/client/" + str(client) + "/upload/" + str(upload)
    header = {'x-api-key': key,
              'Content-Type': "application/json",
              'Cache-Control': "no-cache"
              }

    raw_check_upload_state_response = requests.get(url, headers=header)
    json_check_upload_state_response = json.loads(raw_check_upload_state_response.text)

    if raw_check_upload_state_response.status_code == 200:
        state = json_check_upload_state_response['state']
        logging.debug("State: %s", state)

    else:
        print(f"An error has occurred while attempting to check the state of your upload.")
        logging.info("An error has occurred while attempting to check the state of the upload.")
        print(f"Status Code returned was {raw_check_upload_state_response.status_code}")
        logging.info("Status Code returned was: %s", raw_check_upload_state_response.status_code)

        return "ERROR"

    return state


############################################################
#
#  Read Configuration File
#
############################################################
def read_config_file(filename):

    print()
    print("Reading configuration file...")

    try:
        toml_data = open(filename).read()
    except:
        print("Error reading configuration file.  Please check for formatting errors.")
        exit()

    data = toml.loads(toml_data)
    logging.debug("Loaded configuration: %s", data)

    return data


##########################################################
#
#  MAIN BODY
#
##########################################################

conf_file = "config.toml"
config = read_config_file(conf_file)

# Specify Settings For the Log
logging.basicConfig(filename=config['path_to_logs']+'/uploads.log',level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

rs_platform = config["platform"]
api_key = config["api-key"]

if len(sys.argv) > 1:
    files = list(sys.argv)
    files.pop(0)

else:
    path_to_files = config["path_to_files"]
    files = [f for f in os.listdir(path_to_files) if os.path.isfile(os.path.join(path_to_files, f))]

logging.info(" *** Configuration read.  Starting Script. ***")

# If no files are found, log, notify the user and exit.
if len(files) == 0:
    print("No files found to process.  Exiting...")
    logging.info("No files found to process.")
    exit()

process_state = ""

today = datetime.date.today()
current_time = time.time()

logging.info("Date: %s", today)
logging.info("Time: %s", current_time)

assessment_name = "assmnt_" + str(today) + "_" + str(current_time)
assessment_start_date = str(today)
assessment_notes = "Assessment generated via REST API script."

print()
print("This tool will now create a new assessment and upload files for scanning...")
print("")

client_id = get_client_id(rs_platform, api_key)

if config["network_id"] != "":
    network_id = config["network_id"]

else:
    network_id = find_network_id(rs_platform, api_key, client_id)

assessment_id = create_new_assessment(rs_platform, api_key, client_id, assessment_name, assessment_start_date, assessment_notes)
upload_id = create_upload(rs_platform, api_key, assessment_id, network_id, client_id)


# Log pertinent session information
logging.info("")
logging.info(" ------- Session Info ---------")
logging.info(" Client ID: %s ", client_id)
logging.info(" Network ID: %s ", network_id)
logging.info(" Assessment Name: %s", assessment_name)
logging.info(" Assessment ID: %s", assessment_id)
logging.info(" Assessment Start Date: %s", assessment_start_date)
logging.info(" Assessment Notes: %s", assessment_notes)
logging.info(" Upload ID: %s", upload_id)
logging.info(" Path to Files: %s", path_to_files)
logging.info(" Files: %s", files)
logging.info(" -----------------------------")
print()

if len(sys.argv) == 1:
    for file in files:
        add_file_to_upload(rs_platform, api_key, client_id, upload_id, file, path_to_files)
        shutil.move(path_to_files + "/" + file, path_to_files + "/archive/" + file)

else:
    x = 0
    while x < len(files):
        files[x] = {"file_path": os.path.dirname(files[x]),
                    "file_name": os.path.basename(files[x])
                    }

        if files[x]['file_name'] != "config.toml":
            add_file_to_upload(rs_platform, api_key, client_id, upload_id, files[x]['file_name'], files[x]['file_path'])
            shutil.move(files[x]['file_path'] + "/" + files[x]['file_name'], files[x]['file_path'] + "/archive/" + files[x]['file_name'])
        x += 1

print("")
print("Beginning processing of uploaded files.")
print()
print(" *  The RiskSense Platform is now processing your uploaded files. If you prefer  *")
print(" *  not to wait, you may hit CTRL+C now to end the script if you would rather    *")
print(" *  check the status by manually logging in to the RiskSense platform later.     *")
print()

begin_processing(rs_platform, api_key, client_id, upload_id)
time.sleep(15)

while process_state != "COMPLETE":
    process_state = check_upload_state(rs_platform, api_key, client_id, upload_id)

    if process_state != "COMPLETE":
        print(f"Process state is {process_state}. Please wait...")

    elif process_state == "ERROR":
        break

    time.sleep(15)

print()
print(f"Processing of uploaded file(s) has ended. State: {process_state}")
logging.info("Processing of uploaded files has ended.  State: %s", process_state)

hold_open = input("Hit ENTER to close.")
