""" *******************************************************************************************************************
|
|  Name         :  __exports.py
|  Module       :  risksense_api
|  Description  :  A class to be used for interacting with RiskSense platform exports.
|  Copyright    :  (c) RiskSense, Inc.
|  License      :  Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

import json
from ...__subject import Subject
from ..._api_request_handler import *


class ExportFileType:
    """ ExportFileType class and params"""
    CSV = "CSV"
    XML = "XML"
    XLSX = "XLSX"


class Exports(Subject):

    """ Exports class """

    def __init__(self, profile):

        """
        Initialization of Exports object.

        :param profile:     Profile Object
        :type  profile:     _profile

        """

        Subject.__init__(self, profile, Subject.EXPORT)

    def check_status(self, export_id, client_id=None):

        """
        Checks on the status of an export.

        :param export_id:   The ID of the export to be checked.
        :type  export_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    A string reflecting the status of the export is returned.
        :rtype:     str

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/status".format(str(export_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        export_status = jsonified_response['status']

        return export_status

    def download_export(self, export_id, filename, client_id=None):

        """
        Download an exported file.

        :param export_id:   The ID of the export.
        :type  export_id:   int

        :param filename:    The filename to save the downloaded file as.
        :type  filename:    str

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflects whether or not the download was successful.
        :rtype:     bool

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises FileNotFoundError:
        :raises Exception:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(export_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)

        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        try:
            open(filename, "wb").write(raw_response.content)

        except (FileNotFoundError, Exception):
            raise

        success = True

        return success

    def delete_files(self, export_id, client_id=None):

        """
        Delete files related to an export.

        :param export_id:   The export ID.
        :type  export_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the file deletion was successful.
        :rtype:     bool

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(export_id))

        try:
            self.request_handler.make_request(ApiRequestHandler.DELETE, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        success = True

        return success


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
