""" *******************************************************************************************************************
|
|  Name        :  __rosa.py
|  Description :  ROSA
|  Project     :  risksense_api
|  Copyright   :  2019 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import json
from ...__subject import Subject
from ..._api_request_handler import *


class Rosa(Subject):

    """ Rosa Class """

    def __init__(self, profile):
        """
       Initialization of ROSA object.

       :param profile:     Profile Object
       :type  profile:     _profile
       """

        self.subject_name = "rosa"
        Subject.__init__(self, profile, self.subject_name)

    def create(self, rosa_name, client_id=None):

        """
        Create a new ROSA

        :param rosa_name:   ROSA Name
        :type  rosa_name:   str

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The new ROSA's ID
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(client_id)

        body = {
            "name": rosa_name
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        rosa_id = jsonified_response['id']

        return rosa_id

    def get_rosas(self, page_size=150, page_num=0, client_id=None):

        """
        Get a paginated list of ROSAs in a client

        :param page_size:   Page Size
        :type  page_size:   int

        :param page_num:    Page Number
        :type  page_num:    int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(client_id)

        params = {
            "page": page_num,
            "size": page_size
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url, params=params)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_single_rosa(self, rosa_id, client_id=None):

        """

        :param rosa_id:     ROSA ID
        :type  rosa_id:     int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    The ROSA's details
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(client_id) + "/{}".format(str(rosa_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def update(self, rosa_id, name=None, enabled=None, log_fwd_enabled=None, update_interval=None, client_id=None):

        """

        :param rosa_id:             ROSA ID
        :type  rosa_id:             int

        :param name:                Name for the ROSA
        :type  name:                str

        :param enabled:             Enable ROSA
        :type  enabled:             bool

        :param log_fwd_enabled:     Enable log forwarding
        :type  log_fwd_enabled:     bool

        :param update_interval:     Update Interval
        :type  update_interval:     int

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    Job ID
        :rtype:     int

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises: ValueError
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(client_id) + "/{}".format(str(rosa_id))

        body = {
            "name": name,
            "enabled": enabled,
            "logForwardingEnabled": log_fwd_enabled,
            "updateInterval": update_interval
        }

        body = self._strip_nones_from_dict(body)

        if body == {}:
            raise ValueError("At one of the following values is required: name, enabled, log_fwd_enabled, update_interval")

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.PUT, url, body=body)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def delete(self, rosa_id, client_id=None):

        """
        Delete a ROSA

        :param rosa_id:     ROSA ID
        :type  rosa_id:     int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    Indication of success
        :rtype:     bool

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(client_id) + "/{}".format(str(rosa_id))

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.DELETE, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        successful = True

        if 'id' not in raw_response.text:
            successful = False

        return successful

    def get_config(self, rosa_id, client_id=None):

        """
        Get the configuration of a ROSA.

        :param rosa_id:     ROSA ID
        :type  rosa_id:     int

        :param client_id:   Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:   int

        :return:    Response text
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(client_id) + "/{}/configuration".format(str(rosa_id))

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
