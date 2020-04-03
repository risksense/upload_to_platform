""" *******************************************************************************************************************
|
|  Name         :  upload_to_platform.py
|  Project      :  Upload to Platform
|  Description  :  Uploads files to the RiskSense platform, and kicks off the processing of those files.
|  Version      :  1.0
|  Copyright    :  (c) RiskSense, Inc.
|  License      :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import time
import shutil
import datetime
import sys
import os
import logging
import argparse
import toml
from toml import TomlDecodeError
import progressbar
from packages import risksense_api as rsapi

__version__ = "1.0"
USER_AGENT_STRING = "upload_to_platform_v" + __version__


class UploadToPlatform:

    """ UploadToPlatform class """

    def __init__(self):

        """ Initialize UploadToPlatform class, and upload scan files """

        today = datetime.date.today()
        current_time = time.time()

        print(f"\n\n         *** RiskSense -- {USER_AGENT_STRING} ***")
        print('Upload scan files to the RiskSense platform via the RiskSense API.')
        print("------------------------------------------------------------------\n")

        #  Read the config
        conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'config.toml')
        config = self.read_config_file(conf_file)

        #  Process any args passed by the user, and set variables appropriately.
        args = self.arg_parser_setup(config)
        rs_platform, api_key, file_path, log_folder, auto_urba, client_id, network_id = self.process_args(args)

        #  Specify Settings For the Log
        log_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), log_folder, 'uploads.log')
        logging.basicConfig(filename=log_file, level=logging.DEBUG,
                            format='%(levelname)s:  %(asctime)s > %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.info("Date: %s", today)
        logging.info("Time: %s", current_time)

        #  Create RiskSenseApi instance for communicating with the platform
        self.rs = rsapi.RiskSenseApi(rs_platform, api_key)

        #  Validate client_id provided in args/config or get the user to choose one
        if client_id is not None:
            print("Validating the provided client ID...")
            self.validate_client_id(client_id)
        else:
            client_id = self.get_client_id()
            if client_id == 0:
                print()
                print("Exiting.")
                exit(1)

        #  Set the default client ID in the RiskSenseApi object
        self.rs.set_default_client_id(client_id)

        #  Get the user to choose a Network ID if none was provided in args/config
        if network_id is None:
            network_id = self.find_network_id()
        #  If a network ID was provided in args/config, validate it.
        else:
            self.validate_network_id(network_id)

        # Get info about files available to be uploaded.
        files, path_to_files = self.process_files(file_path)

        #  Start defining parameters for new assessment
        assessment_name = "assmnt_" + str(today) + "_" + str(current_time)
        assessment_start_date = str(today)
        assessment_notes = "Assessment generated via upload_to_platform.py."
        print()
        print(f"Creating a new assessment ({assessment_name})...")

        #  Actual creation of a new Assessment
        assessment_id = self.create_new_assessment(assessment_name, assessment_start_date, assessment_notes)

        #  Start defining parameters for new upload
        upload_name = "upload_" + str(today) + "_" + str(current_time)
        print(f"Creating a new upload ({upload_name})...")
        print()

        #  Actual creation of a new Upload
        upload_id = self.create_new_upload(upload_name, assessment_id, network_id)

        #  Log session info in log file
        self.log_session_info(network_id, auto_urba, assessment_name, assessment_id, assessment_start_date,
                              assessment_notes, upload_id, path_to_files, files)

        #  Start uploading files
        print("Uploading File(s)...")
        num_upload_errors = self.upload_files(upload_id, files, path_to_files)

        #  If the number of upload errors is less than the number of files, start processing them.
        if num_upload_errors < len(files):
            self.begin_upload_processing(upload_id, auto_urba)
        else:
            print(f"There were no files that were successfully uploaded.  Exiting.")
            print()
            input("Hit ENTER to close.")
            exit(1)

        #  Begin monitoring processing of the uploaded files until complete
        print("Now monitoring the processing state of your uploaded files...")
        time.sleep(15)
        process_state = ""

        while process_state != "COMPLETE":
            process_state = self.check_processing_state(upload_id)
            if process_state == "ERROR":
                break
            if process_state == "COMPLETE":
                break
            else:
                print(f"Process state is currently: {process_state}.")
                time.sleep(15)

        print()
        processing_finished_msg = "Processing of uploaded file(s) has ended. State: {}".format(process_state)
        if auto_urba:
            processing_finished_msg += "\nRiskSense will now begin the Update Remediation By Assessment (URBA) process."
        print(processing_finished_msg)
        logging.info("Processing of uploaded files has ended.  State: %s", process_state)
        print()
        input("Hit ENTER to close.")

    def validate_client_id(self, client):

        """
        Validates that a client ID is associated with the specified API key.

        :param client:      Client ID to verify
        :type  client:      int
        """

        valid_flag = False

        for item in self.rs.my_clients:
            if client == item['id']:
                valid_flag = True

        if valid_flag:
            print(" - Client ID validated.")
            print()
        else:
            message = "Unable to validate client ID provided: " + str(client)
            print(message)
            logging.error(message)
            print(f"Please provide a valid client ID. Exiting...")
            exit(1)

    def validate_network_id(self, network_id):

        """
        Validate the network ID provided by the user in the args/config

        :param network_id:  Network ID to validate
        :type  network_id:  int
        """

        found_networks = None

        network_search_filter = [
            {
                "field": "id",
                "exclusive": False,
                "operator": "EXACT",
                "value": network_id
            }
        ]

        print(f"Validating the provided network ID...")

        try:
            found_networks = self.rs.networks.search(network_search_filter)
        except (rsapi.RequestFailed, rsapi.StatusCodeError) as ex:
            print(f"The search for available networks has failed:")
            print(ex)
            logging.critical("ERROR. The search for available networks has failed:")
            logging.critical(ex)
            exit(1)
        except rsapi.MaxRetryError as ex:
            print(f"The search for available networks has reached the maximum number of retries, and failed:")
            print(ex)
            logging.critical("ERROR. The search for available networks has reached "
                             "the maximum number of retries, and failed:")
            logging.critical(ex)
            exit(1)
        except Exception as ex:
            print("ERROR. There was an unexpected problem getting a list of available networks from the platform.")
            print(ex)
            logging.critical("ERROR. There was an unexpected problem getting a list "
                             "of available networks from the platform.")
            logging.critical("Exception: \n %s", ex)
            exit(1)

        if len(found_networks) != 1:
            print()
            print("The provided network ID appears to be invalid.  Exiting.")
            input("Press ENTER to close.")
            print()
            exit(1)

        print(" - Network ID validated.")

    def find_network_id(self):

        """
        Find the network IDs associated with a client, and have the user
        select which should be used for the upload.

        :return:    The Network ID to associate upload with.
        :rtype:     int
        """

        network = 0
        found_networks = None

        logging.info("Getting Network ID")

        num_networks = self.find_network_count()
        if num_networks == 1:
            network_search_filter = []
        else:
            print("An upload must be associated with a network.")
            print("We will search your networks to help you identify which you would like to use.")
            print()
            search_value = input("Input a search string to search for your desired network name (or hit 'ENTER' to list all available networks): ")
            logging.info("Customer search string: %s", search_value)

            logging.info("Querying networks based on your search string")

            network_search_filter = [
                {
                    "field": "name",
                    "exclusive": False,
                    "operator": "LIKE",
                    "value": search_value
                }
            ]

        try:
            found_networks = self.rs.networks.search(network_search_filter)
        except (rsapi.RequestFailed, rsapi.StatusCodeError) as ex:
            print(f"The search for available networks has failed:")
            print(ex)
            logging.critical("ERROR. The search for available networks has failed:")
            logging.critical(ex)
            exit(1)
        except rsapi.MaxRetryError as ex:
            print(f"The search for available networks has reached the maximum number of retries, and failed:")
            print(ex)
            logging.critical("ERROR. The search for available networks has reached "
                             "the maximum number of retries, and failed:")
            logging.critical(ex)
            exit(1)
        except Exception as ex:
            print("ERROR. There was an unexpected problem getting a list of available networks from the platform.")
            print(ex)
            logging.critical("ERROR. There was an unexpected problem getting a list "
                             "of available networks from the platform.")
            logging.critical("Exception: \n %s", ex)
            exit(1)

        if network_search_filter == [] and len(found_networks == 1):
            return found_networks[0]['id']

        if len(found_networks) == 0:
            print()
            print("No such network found.  Exiting.")
            input("Press ENTER to close.")
            print()
            exit(1)
        elif len(found_networks) >= 1:
            network_list = []
            for z in range(0, len(found_networks)):
                if found_networks[z]['clientId'] == self.rs.get_default_client_id():
                    network_list.append([found_networks[z]['id'], found_networks[z]['name']])

            for y in range(0, len(network_list)):
                print(f"{y} - {network_list[y][1]}")

            list_id = input("Enter the number above that is associated with the network that you would like to select: ")
            network = network_list[int(list_id)][0]

        return network

    def process_args(self, arguments):

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

        if api_key == "":
            self.no_api_key()

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

    def get_client_id(self):

        """
        Get the client IDs associated with the specified API key, and have the user select one.

        :return:    The client ID to be used while uploading the files.
        :rtype:     int
        """

        print("An upload must be associated with a client.  Finding available clients...")
        print()

        #  Sort list all_found_ids by client name.
        sorted_clients = sorted(self.rs.my_clients, key=lambda k: k['name'])

        for x in range(0, len(sorted_clients)):
            print(f"{x} - {sorted_clients[x]['name']}")

        selected_id = input("Enter the number above that is associated with the client that you would like to select: ")

        if selected_id.isdigit() and int(selected_id) >= 0 and int(selected_id) < len(sorted_clients):
            found_id = sorted_clients[int(selected_id)]['id']
            print()
        else:
            print("You have made an invalid selection.")
            found_id = 0

        return found_id

    def find_network_count(self):

        """
        Get the count of available networks

        :return:    Count of available networks
        :rtype:     int
        """

        network_search_filter = []

        try:
            found_networks = self.rs.networks.search(network_search_filter)
            return len(found_networks)

        except (rsapi.RequestFailed, rsapi.StatusCodeError) as ex:
            print(f"The search for network count has failed:")
            print(ex)
            logging.critical("ERROR. The search for available networks has failed:")
            logging.critical(ex)
            exit(1)
        except rsapi.MaxRetryError as ex:
            print(f"The search for network count has reached the maximum number of retries, and failed:")
            print(ex)
            logging.critical("ERROR. The search for network count has reached "
                             "the maximum number of retries, and failed:")
            logging.critical(ex)
            exit(1)
        except Exception as ex:
            print("ERROR. There was an unexpected problem getting a count of available networks from the platform.")
            print(ex)
            logging.critical("ERROR. There was an unexpected problem getting a count "
                             "of available networks from the platform.")
            logging.critical("Exception: \n %s", ex)
            exit(1)

    def create_new_assessment(self, assessment_name, assessment_start_date, assessment_notes):

        """
        Create a new assessment

        :param assessment_name:
        :type  assessment_name:

        :param assessment_start_date:
        :type  assessment_start_date:

        :param assessment_notes:
        :type  assessment_notes:

        :return:
        :rtype:
        """
        assessment_id = None

        try:
            assessment_id = self.rs.assessments.create(assessment_name, assessment_start_date, assessment_notes)
        except (rsapi.RequestFailed, rsapi.StatusCodeError) as ex:
            print(f"The creation of a new assessment has failed:")
            print(ex)
            logging.critical("ERROR. The creation of a new assessment has failed:")
            logging.critical(ex)
            exit(1)
        except rsapi.MaxRetryError as ex:
            print(f"The creation of a new assessment has reached the maximum number of retries, and failed:")
            print(ex)
            logging.critical("ERROR. The creation of a new assessment has reached "
                             "the maximum number of retries, and failed:")
            logging.critical(ex)
            exit(1)
        except Exception as ex:
            print("ERROR. There was an unexpected problem creating a new assessment.")
            print(ex)
            logging.critical("ERROR. There was an unexpected problem creating a new assessment.")
            logging.critical("Exception: \n %s", ex)
            exit(1)

        return assessment_id

    def create_new_upload(self, upload_name, assessment_id, network_id):

        """
        Create a new upload

        :param upload_name:     Name for new upload
        :type  upload_name:     str

        :param assessment_id:   Assessment ID to associate upload with
        :type  assessment_id:   int

        :param network_id:      Network ID to associate upload with
        :type  network_id:      int

        :return:    The new upload's ID
        :rtype:     int
        """

        upload_id = None

        try:
            upload_id = self.rs.uploads.create(upload_name, assessment_id, network_id)
        except (rsapi.RequestFailed, rsapi.StatusCodeError) as ex:
            print(f"The creation of a new upload has failed:")
            print(ex)
            logging.critical("ERROR. The creation of a new upload has failed:")
            logging.critical(ex)
            exit(1)
        except rsapi.MaxRetryError as ex:
            print(f"The creation of a new upload has reached the maximum number of retries, and failed:")
            print(ex)
            logging.critical("ERROR. The creation of a new upload has reached "
                             "the maximum number of retries, and failed:")
            logging.critical(ex)
            exit(1)
        except Exception as ex:
            print("ERROR. There was an unexpected problem creating a new upload.")
            print(ex)
            logging.critical("ERROR. There was an unexpected problem creating a new upload.")
            logging.critical("Exception: \n %s", ex)
            exit(1)

        return upload_id

    def upload_files(self, upload_id, files, path_to_files):

        """
        Upload files to RiskSense.

        :param upload_id:       Upload ID
        :type  upload_id:       int

        :param files:           List of dicts indicating files to upload
        :type  files:           list

        :param path_to_files:   Path to files
        :type  path_to_files:   Path to location on disk where files exist

        :return:    Number of upload errors that occurred
        :rtype:     int
        """

        upload_errors = 0

        with progressbar.ProgressBar(max_value=len(files)) as bar:
            bar_counter = 1
            for file in files:
                try:
                    self.rs.uploads.add_file(upload_id, file['name'], path_to_file=file['full_path'])
                except FileNotFoundError as fnfe:
                    upload_errors += 1
                    print(f"Unable to find file {file['name']} for upload.  Moving on.")
                    logging.critical("Unable to find file %s for upload", file['name'])
                    logging.critical(fnfe)
                    continue
                except (rsapi.RequestFailed, rsapi.StatusCodeError) as ex:
                    upload_errors += 1
                    print(f"Uploading {file['name']} has failed:")
                    print(ex)
                    logging.critical("Uploading %s has failed::", file['name'])
                    logging.critical(ex)
                    continue
                except rsapi.MaxRetryError as ex:
                    upload_errors += 1
                    print(f"Uploading {file['name']} has failed after reaching the maximum number of retries:")
                    print(ex)
                    logging.critical("Uploading file %s has failed after reaching the maximum number of retries", file['name'])
                    logging.critical(ex)
                    continue
                except Exception as ex:
                    upload_errors += 1
                    print(f"ERROR. There was an unexpected problem while trying to upload file {file['name']}")
                    print(ex)
                    logging.critical("ERROR. There was an unexpected problem while trying to upload file %s", file['name'])
                    logging.critical(ex)
                    continue

                shutil.move(path_to_files + "/" + file['name'], path_to_files + "/archive/" + file['name'])
                bar.update(bar_counter)
                time.sleep(0.1)
                bar_counter += 1

        return upload_errors

    def begin_upload_processing(self, upload_id, auto_urba):

        """
        Begin processing the uploaded files

        :param upload_id:   Upload ID
        :type  upload_id:   int

        :param auto_urba:   Auto URBA
        :type  auto_urba:   bool
        """

        print()
        try:
            self.rs.uploads.start_processing(upload_id, auto_urba)
            print(" **        The RiskSense platform is now processing your uploaded files.        **")
            print(" **                                                                             **")
            print(" **  If you prefer not to monitor the status of the processing of your files,   **")
            print(" **  you may hit CTRL+C now to end the script. You can always check the status  **")
            print(" **  by manually logging in to the RiskSense platform at any time.              **")
            print()
        except (rsapi.RequestFailed, rsapi.StatusCodeError, rsapi.MaxRetryError, Exception):
            print(f"There was an unexpected issue starting the processing of your files.  Please log in"
                  f"to the platform and start the processing manually. ")
            input("Hit ENTER to close.")
            exit(1)

    def check_processing_state(self, upload_id):

        """
        Check the processing state of the upload.

        :param upload_id:   Upload ID
        :type  upload_id:   int

        :return:    Process state
        :rtype:     str
        """

        try:
            process_state = self.rs.uploads.check_state(upload_id)
            return process_state
        except (rsapi.RequestFailed, rsapi.StatusCodeError, rsapi.MaxRetryError, Exception):
            print(f"An unexpected issue has occurred while trying to check the state of your upload.")
            print(f"Please log in to the platform to monitor the status of this upload.")
            input("Hit ENTER to close.")
            exit(1)

    def log_session_info(self, network_id, auto_urba, assessment_name, assessment_id,
                         assessment_start_date, assessment_notes, upload_id, path_to_files, files):

        """
        Log the info for the upload session.

        :param network_id:              Network ID
        :type  network_id:              int

        :param auto_urba:               Auto URBA
        :type  auto_urba:               bool

        :param assessment_name:         Assessment Name
        :type  assessment_name:         str

        :param assessment_id:           Assessment ID
        :type  assessment_id:           int

        :param assessment_start_date:   Assessment Start Date
        :type  assessment_start_date:   str

        :param assessment_notes:        Assessment Notes
        :type  assessment_notes:        str

        :param upload_id:               Upload ID
        :type  upload_id:               int

        :param path_to_files:           Path to folder containing files
        :type  path_to_files:           str

        :param files:                   List of files
        :type  files:                   list
        """

        #  Write session info to log file.
        logging.info("")
        logging.info(" ------- Session Info ---------")
        logging.info(" Client ID: %s ", self.rs.get_default_client_id())
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
        logging.info("")

    @staticmethod
    def no_api_key():

        """ No API Key was found.  Print message acknowledging, and exit. """

        message = "No API Key configured.  \n " \
                  "Please supply an API Key by one of the following methods: \n" \
                  " - Add to the configuration file (conf/config.toml) \n" \
                  " - Provide as an argument when executing script."
        print(message)
        logging.info(message)
        input("Please press ENTER to close.")
        exit(1)

    @staticmethod
    def process_files(file_path):

        """
        Check for files to upload, and compile the information

        :param file_path:   Location to check for files.
        :type  file_path:   str

        :return:    list of files, and full path on disk to the folder they are in
        :rtype:     tuple
        """

        files = []

        if file_path == "files_to_process":
            path_to_files = os.path.join(os.path.abspath(os.path.dirname(__file__)), file_path)
        else:
            path_to_files = file_path

        #  Get filenames, but ignore subfolders.
        filenames = [f for f in os.listdir(path_to_files) if os.path.isfile(os.path.join(path_to_files, f))]

        for x in range(0, len(filenames)):
            if filenames[x] == "PLACE_FILES_TO_SCAN_HERE.txt":
                continue
            else:
                files.append({"name": filenames[x], "full_path": os.path.join(path_to_files, filenames[x])})

        #  If no files are found, log, notify the user, and exit.
        if len(filenames) == 0:
            message = "No files found to process.  Exiting..."
            print()
            print(message)
            logging.info(message)
            print()
            input("Please press ENTER to close.")
            exit(1)

        return files, path_to_files

    @staticmethod
    def arg_parser_setup(config):

        """
        Set up the valid args for the arg parser

        :param config:  Config variables
        :type  config:  dict

        :return:    Args
        :rtype:
        """

        parser = argparse.ArgumentParser(description='The following arguments can be used to override those in the config file:',
                                         formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=60))
        parser.add_argument('-p', '--platform', help='Platform URL', type=str, required=False, default=config['platform'])
        parser.add_argument('-a', '--api_key', help='API Key', type=str, required=False, default=config['api-key'])
        parser.add_argument('-f', '--files_folder', help='Path to folder containing scan files', type=str, required=False, default=config['files_folder'])
        parser.add_argument('-l', '--log_folder', help='Path to folder to write log', type=str, required=False, default=config['log_folder'])
        parser.add_argument('-u', '--auto_urba', help='Run auto-URBA?', type=str, choices=["true", "false"], required=False, default=config['auto_urba'])
        parser.add_argument('-c', '--client_id', help='Client ID', type=int, required=False, default=config['client_id'])
        parser.add_argument('-n', '--network_id', help='Network ID', type=int, required=False, default=config['network_id'])

        args = parser.parse_args()

        return args

    @staticmethod
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
        except TomlDecodeError as tde:
            print("An error occurred while trying to decode your config file.  Please check it for formatting errors.")
            print(f"\n{tde}\n")
            input("Please press ENTER to close.")
            exit(1)
        except FileNotFoundError as fnfe:
            print("An error occurred while trying to locate your config file. "
                  "Please verify that it exists in the \"conf\" folder.")
            print(f"\n{fnfe}\n")
            input("Please press ENTER to close.")
            exit(1)
        except Exception as ex:
            print("An unexpected error occurred while trying to read your config file.")
            print(f"\n{ex}\n")
            input("Please press ENTER to close.")
            exit(1)

        data = toml.loads(toml_data)

        if "client_id" not in data:
            data.update({"client_id": None})
        if "network_id" not in data:
            data.update({"network_id": None})

        return data


#  Execute Script
if __name__ == "__main__":
    try:
        UploadToPlatform()
    except KeyboardInterrupt:
        print()
        print("KeyboardInterrupt detected.  Exiting...")
        print()
        sys.exit(0)


"""
   Copyright 2020 RiskSense, Inc.
   
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