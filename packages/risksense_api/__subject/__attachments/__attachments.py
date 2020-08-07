""" *******************************************************************************************************************
|
|  Name        :  __attachments.py
|  Module      :  risksense_api
|  Description :  A class to be used for interacting with tag attachments on the RiskSense Platform.
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import json
from ...__subject import Subject
from ..._api_request_handler import *


class Attachments(Subject):

    """ Attachments class """

    def __init__(self, profile):

        """
        Initialization of Attachments object.

        :param profile:     Profile Object
        :type  profile:     _profile

        """

        self.subject_name = "attachment"
        Subject.__init__(self, profile, self.subject_name)
        self.api_base_url += "/tag/{}/"

    def upload(self, tag_id, file_name, client_id=None):

        """
        Upload a new attachment for a tag.

        :param tag_id:      The tag ID.
        :type  tag_id:      int

        :param file_name:   The file to be uploaded.
        :type  file_name:   str

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The UUID of the uploaded file is returned.
        :rtype:     str

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id), str(tag_id)) + "/attachment"

        upload_file = {'attachments': (file_name, open(file_name, 'rb'))}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=upload_file)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        file_uuid = jsonified_response['uuid']

        return file_uuid

    def list_attachments(self, tag_id, client_id=None):

        """
        List the attachment(s) associated with a tag.

        :param tag_id:          The tag ID.
        :type  tag_id:          int

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id), str(tag_id)) + "/attachment"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_attachment(self, tag_id, attachment_uuid, file_destination, client_id=None):

        """
        Get an attachment associated with a tag.

        :param tag_id:              Integer.  The tag ID.
        :type  tag_id:              int

        :param attachment_uuid:     String.  The UUID for the attachment to be downloaded.
        :type  attachment_uuid:     str

        :param file_destination:    String.  The location to save the attachment locally.
        :type  file_destination:    str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    A True/False is returned reflecting whether or not the operation was successful.
        :rtype:     bool

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises FileNotFoundError:
        :raises Exception:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id), str(tag_id)) + "/attachment/" + str(attachment_uuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        try:
            open(file_destination, "wb").write(raw_response.content)
        except (FileNotFoundError, Exception):
            raise

        success = True

        return success

    def delete(self, tag_id, attachment_uuid, client_id=None):

        """
        Delete an attachment associated with a tag.

        :param tag_id:              The tag ID.
        :type  tag_id:              int

        :param attachment_uuid:     The UUID for the attachment to be deleted.
        :type  attachment_uuid:     str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID is returned
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id), str(tag_id)) + "/attachment/" + str(attachment_uuid)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        returned_id = jsonified_response['id']

        return returned_id

    def get_metadata(self, tag_id, attachment_uuid, client_id=None):

        """
        Get the metadata associated with an attachment.

        :param tag_id:              The tag ID.
        :type  tag_id:              int

        :param attachment_uuid:     The UUID for the attachment to be deleted.
        :type  attachment_uuid:     str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The JSON response from the platform containing the metadata is returned.
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id), str(tag_id)) + "/attachment/" + str(attachment_uuid) + "/meta"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response


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
