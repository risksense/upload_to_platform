""" *******************************************************************************************************************
|
|  Name        : __uploads.py
|  Module      : risksense_api
|  Description : A class to be used for interacting with uploads on the RiskSense Platform.
|  Copyright   : (c) RiskSense, Inc.
|  License     : Apache-2.0  (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

import json
from ...__subject import Subject
from ..._api_request_handler import *


class Uploads(Subject):

    """ Uploads class """

    def __init__(self, profile):

        """
        Initialization of Uploads object.

        :param profile:     Profile Object
        :type  profile:     _profile
        """

        Subject.__init__(self, profile, Subject.UPLOAD)

    def get_uploads(self, assessment_id, page_num=0, page_size=150, client_id=None):

        """
        Get uploads associated with an assessment.

        :param assessment_id:   The assessment ID.
        :type  assessment_id:   int

        :param page_num:        The page number of results to return.
        :type  page_num:        int

        :param page_size:       The number of results per page to return.
        :type  page_size:       int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises PageSizeError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        params = {
            "assessmentId": assessment_id,
            "size": page_size,
            "page": page_num
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url, params=params)
        except (RequestFailed, StatusCodeError, MaxRetryError, PageSizeError):
            raise

        jsonified_response = json.dumps(raw_response.text)

        return jsonified_response

    def create(self, name, assessment_id, network_id, client_id=None):

        """
        Create a new upload.

        :param name:            The name to be associated with the upload.
        :type  name:            str

        :param assessment_id:   The assessment ID.
        :type  assessment_id:   int

        :param network_id:      The network ID.
        :type  network_id:      int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The Upload ID
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id))

        body = {
            "assessmentId": assessment_id,
            "networkId": network_id,
            "name": name
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        upload_id = jsonified_response['id']

        return upload_id

    def check_state(self, upload_id, client_id=None):

        """
        Check the state of an upload.

        :param upload_id:   The upload ID.
        :type upload_id:    int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The current state of the upload is returned.
        :rtype:     str

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(upload_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        state = jsonified_response['state']

        return state

    def update(self, upload_id, client_id=None, **kwargs):

        """
        Update an upload.  Uploads can only be updated before they have been processed.

        :param upload_id:   The upload ID.
        :type  upload_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword name:              str     Name of upload
        :keyword assessment_id:     int     Assessment ID.
        :keyword network_id:        int     Network ID.

        :return:    The job ID is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(upload_id))

        name = kwargs.get('name', None)
        assessment_id = kwargs.get('assessment_id', None)
        network_id = kwargs.get('network_id', None)

        body = {
            "name": name,
            "assessmentId": assessment_id,
            "networkId": network_id
        }

        body = self._strip_nones_from_dict(body)

        if body == {}:
            raise ValueError("Body is empty.  Please provide name, assessment_id, and/or network_id")

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def delete(self, upload_id, client_id=None):

        """
        Delete an Upload.

        :param upload_id:   The upload ID
        :type  upload_id:   int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}".format(str(upload_id))

        try:
            self.request_handler.make_request(ApiRequestHandler.DELETE, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        success = True

        return success

    def list_files(self, upload_id, page_num=0, page_size=150, client_id=None):

        """
        List files in an upload.

        :param upload_id:  The upload ID
        :type  upload_id:  int

        :param page_num:   The page number to be returned.
        :type  page_num:   int

        :param page_size:  The number of results to return per page.
        :type  page_size:  int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    A paginated JSON response from the platform.
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises PageSizeError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/file".format(str(upload_id))

        params = {
            "size": page_size,
            "page": page_num
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url, params=params)
        except (RequestFailed, StatusCodeError, MaxRetryError, PageSizeError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def add_file(self, upload_id, file_name, path_to_file, client_id=None):

        """
        Add a file to an upload.

        :param upload_id:   Upload ID
        :type  upload_id:   int

        :param file_name:   The name to be used for the uploaded file.
        :type  file_name:   str

        :param path_to_file:   Full path to the file to be uploaded.
        :type  path_to_file:   str

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The file ID is returned.
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises FileNotFoundError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/file".format(str(upload_id))

        upload_file = {'scanFile': (file_name, open(path_to_file, 'rb'))}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=upload_file)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise
        except FileNotFoundError:
            raise

        jsonified_response = json.loads(raw_response.text)
        file_id = jsonified_response[0]['id']

        return file_id

    def update_file(self, upload_id, file_id, client_id=None, **kwargs):

        """
        Update an uploaded file.  Will only work if the file has not yet been processed.

        :param upload_id:   The upload ID.
        :type  upload_id:   int

        :param file_id:     The file ID.
        :type  file_id:     str

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :keyword assessment_id:     The assessment ID the upload should be associated with.  Integer.
        :keyword network_id:        The network ID the upload should be associated with.  Integer.
        :keyword application_id:    The application ID the upload should be associated with.  Integer.

        :return:    The upload ID is returned
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises ValueError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/file/{}".format(str(upload_id), str(file_id))

        assessment_id = kwargs.get('assessment_id', None)
        network_id = kwargs.get('network_id', None)
        application_id = kwargs.get('application_id', None)

        body = {
            "assessmentId": assessment_id,
            "networkId": network_id,
            "applicationId": application_id
        }

        body = self._strip_nones_from_dict(body)

        if body == {}:
            raise ValueError('Body empty. Please provide assessment_id, network_id, and/or application_id missing.')

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response)
        returned_id = jsonified_response['id']

        return returned_id

    def delete_file(self, upload_id, file_id, client_id=None):

        """
        Delete an uploaded file.

        :param upload_id:   The upload ID.
        :type  upload_id:   int

        :param file_id:     The file ID.
        :type  file_id:     int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successfully submitted.
        :rtype:     bool

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/file/{}".format(str(upload_id), str(file_id))

        try:
            self.request_handler.make_request(ApiRequestHandler.DELETE, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        success = True

        return success

    def download_file(self, upload_id, file_destination, client_id=None):

        """
        Download a previously uploaded file.

        :param upload_id:           The upload ID
        :type  upload_id:           int

        :param file_destination:    The local destination for the downloaded file.
        :type  file_destination:    str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises FileNotFoundError:
        :raises FileExistsError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/file/download".format(str(upload_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        try:
            open(file_destination, "wb").write(raw_response.content)
            success = True
        except (FileNotFoundError, FileExistsError):
            raise

        return success

    def fetch_file_by_uuid(self, upload_id, file_uuid, file_destination, client_id=None):

        """
        Download a file by UUID.

        :param upload_id:           The upload ID
        :type  upload_id:           int

        :param file_uuid:           The file UUID
        :type  file_uuid:           str

        :param file_destination:    The local destination for the downloaded file.
        :type  file_destination:    str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    True/False reflecting whether or not the operation was successful.
        :rtype:     bool

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises FileNotFoundError:
        :raises FileExistsError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/file/{}".format(str(upload_id), str(file_uuid))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        try:
            open(file_destination, "wb").write(raw_response.content)
            success = True
        except (FileNotFoundError, FileExistsError):
            raise

        return success

    def start_processing(self, upload_id, auto_urba=False, client_id=None):

        """
        Initiate processing of an upload.

        :param upload_id:   The upload ID
        :type  upload_id:   int

        :param auto_urba:   Indicator for whether or not auto-URBA should be run after upload is processed.
        :type  auto_urba:   bool

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    True/False reflecting whether or not the operation was successfully submitted.
        :rtype:     bool

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/{}/start".format(str(upload_id))

        body = {
            "autoUrba": auto_urba
        }

        try:
            self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
            success = True
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

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
