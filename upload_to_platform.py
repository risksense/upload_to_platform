""" *******************************************************************************************************************
|
|  Name        :  upload_to_platform.py
|  Project     :  Upload to Platform
|  Description :  Uploads files to the RiskSense platform, and kicks off the processing of those files.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import json
import time
import shutil
import datetime
import sys
import os
import logging
import argparse

from api_request_handler import ApiRequestHandler

import toml
import progressbar

__version__ = "0.7.0"

USER_AGENT_STRING = "upload_to_platform_v" + __version__


def get_client_id(platform, key):

    """
    Get the client ID associated with the specified API key.  Does
    not currently support multiplatform users.

    :param platform:    URL of platform
    :type  platform:    str

    :param key:         API key
    :type  key:         str

    :return:    The client ID to be used while uploading the files.
    :rtype:     int
    """

    print(f"Determining available Client IDs...")
    print()

    request_handler = ApiRequestHandler(key, user_agent=USER_AGENT_STRING)

    url = platform + "/api/v1/client?size=300"

    raw_client_id_response = None

    try:
        raw_client_id_response = request_handler.make_request("GET", url)

    except Exception as ex:
        message = "ERROR.  There was a problem trying to get a list of available client IDs.  Exiting."
        print(message)
        print(ex)

        logging.critical(message)
        logging.critical(ex)
        exit(1)

    if request_handler.valid_response(raw_client_id_response, 200):

        json_client_id_response = json.loads(raw_client_id_response.text)

        if json_client_id_response['page']['totalElements'] == 1:
            found_id = json_client_id_response['_embedded']['clients'][0]['id']

        else:
            all_found_ids = json_client_id_response['_embedded']['clients']
            print()
            print("These are the available Client IDs associated with your account. ")
            print("You will need to select which of your clients to associate this upload with.")
            print()

            #  Sort list all_found_ids by client name.
            all_found_ids = sorted(all_found_ids, key=lambda k: k['name'])

            x = 0
            while x < len(all_found_ids):
                print(f"{x} - {all_found_ids[x]['name']}")
                x += 1

            selected_id = input("Enter the number above that is associated with the client that you would like to select: ")

            if selected_id.isdigit() and int(selected_id) >= 0 and int(selected_id) < len(all_found_ids):
                found_id = all_found_ids[int(selected_id)]['id']
                print()
            else:
                print("You have made an invalid selection.")
                found_id = 0

    else:
        print()
        print("Unable to retrieve Client IDs.  Exiting.")
        print(f"Status Returned: {raw_client_id_response.status_code}")
        print(raw_client_id_response.text)
        found_id = 0
        print()
        exit(1)

    return found_id


def validate_client_id(client, platform, key):

    """
    Validates that a client ID is associated with the specified
    API key.

    :param client:      Client ID to verify
    :type  client:      int

    :param platform:    URL of platform
    :type  platform:    str

    :param key:         API key
    :type  key:         str

    :return:    Indication as to whether or not the client ID is valid.
    :rtype:     bool
    """

    request_handler = ApiRequestHandler(key, user_agent=USER_AGENT_STRING)

    validity = False

    url = platform + "/api/v1/client/" + str(client)

    raw_client_id_response = None

    try:
        raw_client_id_response = request_handler.make_request("GET", url)

    except Exception as ex:
        print("ERROR. There was a problem validating the client ID.")
        print(ex)

        logging.critical("ERROR. There was a problem validating the client ID. (Client ID: %s)", client)
        logging.critical("Exception: \n %s", ex)

        exit(1)

    if request_handler.valid_response(raw_client_id_response, 200):
        json_client_id_response = json.loads(raw_client_id_response.text)

        if json_client_id_response['id'] == client:
            validity = True

    return validity


def find_network_id(platform, key, client):

    """
    Find the network IDs associated with a client, and have the user
    select which should be used for the upload.

    :param platform:    URL of platform
    :type  platform:    str

    :param key:         API key
    :type  key:         str

    :param client:      Client ID
    :type  client:      int

    :return:    The selected Network ID
    :rtype:     int
    """

    request_handler = ApiRequestHandler(key, user_agent=USER_AGENT_STRING)

    network = 0

    logging.info("Getting Network ID")

    print()
    print("An upload must be associated with a network.")
    network_id_known = input("Do you happen to know the network ID for your upload? (y/n) ")
    print()
    logging.info("Does customer know network ID? %s", network_id_known)

    if network_id_known.lower() == 'y':
        network = input("Input network ID: ")
        return network

    else:
        print(f"We will search your networks to help you identify which to use.")
        print()
        search_value = input("Input search string for Network name search (or hit 'ENTER' to list all): ")
        logging.info("Customer search string: %s", search_value)

        logging.info("Querying network IDs based on search string")

        url = platform + "/api/v1/client/" + str(client) + "/network/search"

        body = {
            "filters": [
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

        raw_network_search_response = None

        try:
            raw_network_search_response = request_handler.make_request("POST", url, body=body)

        except Exception as ex:
            print("ERROR. There was a problem getting a list of available networks from the platform.")
            print(ex)

            logging.critical("ERROR. There was a problem getting a list of available networks from the platform.")
            logging.critical("Exception: \n %s", ex)

            exit(1)

        if request_handler.valid_response(raw_network_search_response, 200):
            json_network_search_response = json.loads(raw_network_search_response.text)

            if json_network_search_response['page']['totalElements'] != 0:
                z = 0
                network_list = []
                while z < len(json_network_search_response['_embedded']['networks']):
                    if json_network_search_response['_embedded']['networks'][z]['clientId'] == client:
                        network_list.append([json_network_search_response['_embedded']['networks'][z]['id'],
                                             json_network_search_response['_embedded']['networks'][z]['name']])
                    z += 1

                y = 0
                while y < len(network_list):
                    print(f"{y} - {network_list[y][1]}")
                    y += 1

                list_id = input("Please enter the number that corresponds with your network: ")
                network = network_list[int(list_id)][0]

            else:
                print()
                print("No such network found.")
                input("Press ENTER to close.")
                print()
                exit(1)

        else:
            print(f"An error occurred during the search for your network.  Status code "
                  f"returned was {raw_network_search_response.status_code}")
            return

    return network


def create_new_assessment(platform, key, client, name, start_date, notes):

    """
    Creates a new assessment for the uploaded file(s) to be associated with.

    :param platform:    URL of platform
    :type  platform:    str

    :param key:         API key
    :type  key:         str

    :param client:      Client ID
    :type  client:      int

    :param name:        The name your assessment should be known by.
    :type  name:        str

    :param start_date:  The start date for the assessment
    :type  start_date:  str

    :param notes:       Notes to be associated with the assessment.
    :type  notes:       str

    :return:    The ID that the platform has associated with the created assessment.
    :rtype:     int
    """

    request_handler = ApiRequestHandler(key, user_agent=USER_AGENT_STRING)

    created_id = 0

    logging.info("Creating new assessment.")
    logging.debug("New assessment name: %s", name)
    logging.debug("New assessment start date: %s", start_date)
    logging.debug("New assessment notes: %s", notes)

    url = platform + "/api/v1/client/" + str(client) + "/assessment"

    body = {
        "name": name,
        "startDate": start_date,
        "notes": notes
    }

    raw_assessment_response = None

    try:
        raw_assessment_response = request_handler.make_request("POST", url, body=body)

    except Exception as ex:
        print("ERROR. Unable to create a new assessment.")
        print(ex)

        logging.critical("ERROR. There was a problem creating a new assessment.")
        logging.critical("Exception: \n %s", ex)

        exit(1)

    if request_handler.valid_response(raw_assessment_response, 201):
        json_assessment_response = json.loads(raw_assessment_response.text)
        created_id = json_assessment_response['id']

    else:
        print(f"Error Creating New Assessment.  Status Code returned was {raw_assessment_response.status_code}")

    return created_id


def create_upload(platform, key, assessment, network, client):

    """
    Create an upload to be associated with the assessment.

    :param platform:    URL of platform
    :type  platform:    str

    :param key:         API key
    :type  key:         str

    :param assessment:  Assessment ID to associate the upload with
    :type  assessment:  int

    :param network:     Network ID to associate the upload with
    :type  network:     int

    :param client:      Client ID
    :type  client:      int

    :return:    The ID that the platform has associated with the created upload.
    :rtype:     int
    """

    request_handler = ApiRequestHandler(key, user_agent=USER_AGENT_STRING)

    today = datetime.date.today()
    current_time = time.time()

    logging.info("Creating new upload.")

    upload_name = "upload-" + str(today) + "-" + str(current_time)

    url = platform + "/api/v1/client/" + str(client) + "/upload"

    body = {
        'assessmentId': assessment,
        'networkId': network,
        'name': upload_name
    }

    raw_upload_response = None

    try:
        raw_upload_response = request_handler.make_request("POST", url, body=body)

    except Exception as ex:
        print("ERROR. There was a problem creating a new upload.")
        print(ex)

        logging.critical("ERROR. There was a problem creating a new upload.")
        logging.critical("Exception: \n %s", ex)

        exit(1)

    if request_handler.valid_response(raw_upload_response, 201):
        json_upload_json_response = json.loads(raw_upload_response.text)
        new_upload_id = json_upload_json_response['id']

    else:
        print(f"Error creating new upload.  Status Code returned was {raw_upload_response.status_code}")
        return

    return new_upload_id


def add_file_to_upload(platform, key, client, upload, file_name, file_path):

    """
    Add a scan file to an upload.

    :param platform:    URL of platform
    :type  platform:    str

    :param key:         API key
    :type  key:         str

    :param client:      Client ID
    :type  client:      int

    :param upload:      ID of the upload to associate the file with
    :type  upload:      int

    :param file_name:   Name of the file to be added to the upload
    :type  file_name:   str

    :param file_path:   Path to the file to be added to the upload
    :type  file_path:   str
    """

    request_handler = ApiRequestHandler(key, user_agent=USER_AGENT_STRING)

    logging.info("Adding file to upload: %s", file_name)
    logging.debug("File Path: %s", file_path)

    url = platform + "/api/v1/client/" + str(client) + "/upload/" + str(upload) + "/file"

    upload_file = {'scanFile': (file_name, open(file_path + "/" + file_name, 'rb'))}

    raw_add_file_response = None

    try:
        raw_add_file_response = request_handler.make_request("POST", url, files=upload_file)

    except Exception as ex:
        message = "ERROR. There was a problem adding a file ({})to the upload.".format(file_name)
        print(message)
        print(ex)
        logging.critical(message)
        logging.critical("Exception: \n %s", ex)
        exit(1)

    if not request_handler.valid_response(raw_add_file_response, 201):
        message = "Error uploading file {}.  Status Code returned was {}".format(file_name, raw_add_file_response.status_code)
        print(message)
        print(raw_add_file_response.text)
        logging.info(message)
        logging.info(raw_add_file_response.text)


def begin_processing(platform, key, client, upload, run_urba):

    """
    Begin processing of the files uploaded.

    :param platform:    URL of platform
    :type  platform:    str

    :param key:         API key
    :type  key:         str

    :param client:      Client ID
    :type  client:      int

    :param upload:      ID of the upload to associate the file with
    :type  upload:      int

    :param run_urba:    Indicator whether or not URBA should be run upon completion of processing.
    :type  run_urba:    bool
    """

    request_handler = ApiRequestHandler(key, user_agent=USER_AGENT_STRING)

    logging.info("Starting platform processing")

    url = platform + "/api/v1/client/" + str(client) + "/upload/" + str(upload) + "/start"

    body = {
        "autoUrba": run_urba
    }

    raw_begin_processing_response = None

    try:
        raw_begin_processing_response = request_handler.make_request("POST", url, body=body)

    except Exception as ex:
        message = "ERROR.  There was a problem starting platform processing of the uploaded file(s)."
        print(message)
        print(ex)
        logging.critical(message)
        logging.critical("Exception: \n %s", ex)
        exit(1)

    if request_handler.valid_response(raw_begin_processing_response, 200):
        print("Uploaded file(s) now processing.  This may take a while. Please wait...")

    else:
        print("An error has occurred when trying to start processing of your upload(s).")
        print(raw_begin_processing_response.text)

        logging.info(raw_begin_processing_response.text)


def check_upload_state(platform, key, client, upload):

    """
    Check the state of an upload.

    :param platform:    URL of platform
    :type  platform:    str

    :param key:         API key
    :type  key:         str

    :param client:      Client ID
    :type  client:      int

    :param upload:      ID of the upload to associate the file with
    :type  upload:      int

    :return:    The state of the upload.
    :rtype:     str
    """

    request_handler = ApiRequestHandler(key, user_agent=USER_AGENT_STRING)

    logging.info("Checking status of the upload processing")

    url = platform + "/api/v1/client/" + str(client) + "/upload/" + str(upload)

    try:
        raw_check_upload_state_response = request_handler.make_request("GET", url)

    except Exception as ex:
        print("There was an exception while checking the state of the upload.")
        logging.critical("There was an exception while checking the state of the upload.")
        logging.critical(ex)

        state = "EXCEPTION"
        return state

    if request_handler.valid_response(raw_check_upload_state_response, 200):
        json_check_upload_state_response = json.loads(raw_check_upload_state_response.text)
        state = json_check_upload_state_response['state']
        logging.debug("State: %s", state)

    else:
        print(f"An error has occurred while attempting to check the state of your upload.")
        logging.info("An error has occurred while attempting to check the state of the upload.")

        print(f"Status Code returned was {raw_check_upload_state_response.status_code}")
        logging.info("Status Code returned was: %s", raw_check_upload_state_response.status_code)

        return "ERROR"

    return state


def process_args(arguments):

    """
    Process the arguments that were passed to the script into configuration variables.

    :param arguments:   Arguments received

    :return:    Configuration variable values
    """
    rs_platform = arguments.platform
    api_key = arguments.api_key
    file_path = arguments.files_folder
    log_folder = arguments.log_folder
    client_id = arguments.client_id
    network_id = arguments.network_id

    if arguments.auto_urba == "true":
        auto_urba = True
    elif arguments.auto_urba == "false":
        auto_urba = False
    else:
        auto_urba = arguments.auto_urba

    if client_id is not None:
        client_id = int(client_id)

    if network_id is not None:
        network_id = int(network_id)

    return rs_platform, api_key, file_path, log_folder, auto_urba, client_id, network_id


def read_config_file(filename):

    """
    Reads a TOML-formatted configuration file.

    :param filename:    Path to the TOML-formatted file to be read.
    :type  filename:    str

    :return:  Values contained in config file.
    :rtype:   dict
    """

    toml_data = {}

    try:
        toml_data = open(filename).read()

    except Exception as ex:
        print("Error reading configuration file.  Please check for formatting errors.")
        print()
        print(ex)
        print()
        input("Please press ENTER to close.")
        exit(1)

    data = toml.loads(toml_data)

    return data


def main():

    """ Main body of script """

    print(f"\n\n         *** RiskSense -- {USER_AGENT_STRING} ***")
    print('Upload scan files to the RiskSense platform via the RiskSense API. \n\n')

    conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'config.toml')
    config = read_config_file(conf_file)

    if 'client_id' in config:
        client_id = config['client_id']
    else:
        client_id = None

    if 'network_id' in config:
        network_id = config['network_id']
    else:
        network_id = None

    #  Arg Parsing.  Use values from config file as defaults.
    parser = argparse.ArgumentParser(description='The following arguments can be used to override those in the config file:',
                                     formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=60))
    parser.add_argument('-p', '--platform', help='Platform URL', type=str, required=False, default=config['platform'])
    parser.add_argument('-a', '--api_key', help='API Key', type=str, required=False, default=config['api-key'])
    parser.add_argument('-f', '--files_folder', help='Path to folder containing scan files', type=str, required=False, default=config['files_folder'])
    parser.add_argument('-l', '--log_folder', help='Path to folder to write log', type=str, required=False, default=config['log_folder'])
    parser.add_argument('-u', '--auto_urba', help='Run auto-URBA?', type=str, choices=["true", "false"], required=False, default=config['auto_urba'])
    parser.add_argument('-c', '--client_id', help='Client ID', type=int, required=False, default=client_id)
    parser.add_argument('-n', '--network_id', help='Network ID', type=int, required=False, default=network_id)

    args = parser.parse_args()

    rs_platform, api_key, file_path, log_folder, auto_urba, client_id, network_id = process_args(args)

    log_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), log_folder, 'uploads.log')

    #  Specify Settings For the Log
    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        format='%(levelname)s:  %(asctime)s > %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    if api_key == "":
        message = "No API Key configured.  \n " \
                  "Please supply an API Key by one of the following methods: \n" \
                  " - Add to the configuration file (conf/config.toml) \n" \
                  " - Provide as an argument when executing script."
        print(message)
        logging.info(message)
        input("Please press ENTER to close.")
        exit(1)

    #  Validate client_id or get from API
    if client_id is not None:
        print("Validating the provided client ID...")
        valid = validate_client_id(client_id, rs_platform, api_key)
        if not valid:
            message = "Unable to validate client ID provided: " + str(client_id)
            print(message)
            logging.error(message)
            print(f"Please provide a valid client ID. Exiting...")
            exit(1)
        else:
            print(" - Client ID validated.")
    else:
        client_id = get_client_id(rs_platform, api_key)
        if client_id == 0:
            print()
            print("Exiting.")
            exit(1)

    if file_path == "files_to_process":
        path_to_files = os.path.join(os.path.abspath(os.path.dirname(__file__)), file_path)
    else:
        path_to_files = file_path

    #  Get filenames, but ignore subfolders.
    files = [f for f in os.listdir(path_to_files) if os.path.isfile(os.path.join(path_to_files, f))]

    x = 0
    while x < len(files):
        if files[x] == "PLACE_FILES_TO_SCAN_HERE.txt":
            files.pop(x)
        x += 1

    #  If no files are found, log, notify the user, and exit.
    if len(files) == 0:
        message = "No files found to process.  Exiting..."
        print()
        print(message)
        logging.info(message)
        print()
        input("Please press ENTER to close.")
        exit(1)

    process_state = ""

    today = datetime.date.today()
    current_time = time.time()

    logging.info("Date: %s", today)
    logging.info("Time: %s", current_time)

    assessment_name = "assmnt_" + str(today) + "_" + str(current_time)
    assessment_start_date = str(today)
    assessment_notes = "Assessment generated via upload_to_platform.py."

    if network_id is None:
        network_id = find_network_id(rs_platform, api_key, client_id)

    print()
    print("This tool will now create a new assessment and upload files for scanning.")
    print()

    assessment_id = create_new_assessment(rs_platform, api_key, client_id,
                                          assessment_name, assessment_start_date, assessment_notes)

    upload_id = create_upload(rs_platform, api_key, assessment_id, network_id, client_id)

    #  Log pertinent session information
    logging.info("")
    logging.info(" ------- Session Info ---------")
    logging.info(" Client ID: %s ", client_id)
    logging.info(" Network ID: %s ", network_id)
    logging.info(" Auto URBA: %s ", auto_urba)
    logging.info(" Assessment Name: %s", assessment_name)
    logging.info(" Assessment ID: %s", assessment_id)
    logging.info(" Assessment Start Date: %s", assessment_start_date)
    logging.info(" Assessment Notes: %s", assessment_notes)
    logging.info(" Upload ID: %s", upload_id)
    logging.info(" Path to Files: %s", path_to_files)
    logging.info(" Files: %s", files)
    logging.info(" -----------------------------")
    print()

    print("Uploading Files...")

    with progressbar.ProgressBar(max_value=len(files)) as bar:
        bar_counter = 1

        for file in files:
            add_file_to_upload(rs_platform, api_key, client_id, upload_id, file, path_to_files)
            shutil.move(path_to_files + "/" + file, path_to_files + "/archive/" + file)
            bar.update(bar_counter)
            time.sleep(0.1)
            bar_counter += 1

    print()
    print("Beginning processing of uploaded files.")
    print()
    print(" *  The RiskSense Platform is now processing your uploaded files. If you prefer  *")
    print(" *  not to wait, you may hit CTRL+C now to end the script if you would rather    *")
    print(" *  check the status by manually logging in to the RiskSense platform later.     *")
    print()

    begin_processing(rs_platform, api_key, client_id, upload_id, auto_urba)
    time.sleep(15)

    while process_state != "COMPLETE":
        process_state = check_upload_state(rs_platform, api_key, client_id, upload_id)

        if process_state == "ERROR":
            break

        print(f"Process state is {process_state}. Please wait...")
        time.sleep(15)

    print()
    print(f"Processing of uploaded file(s) has ended. State: {process_state}")
    logging.info("Processing of uploaded files has ended.  State: %s", process_state)

    input("Hit ENTER to close.")


#  Execute Script
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("KeyboardInterrupt detected.  Exiting...")
        print()
        sys.exit(0)


"""
   Copyright 2019 RiskSense, Inc.
   
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at:
   
   http://www.apache.org/licenses/LICENSE-2.0
   
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""