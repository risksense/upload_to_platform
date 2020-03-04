""" *******************************************************************************************************************
|
|  Name        :  __clients.py
|  Module      :  risksense_api
|  Description :  A class to be used for retrieving client information from the RiskSense Platform.
|  Copyright   : (c) RiskSense, Inc.
|  License     : Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import json
from ...__subject import Subject
from ..._api_request_handler import *


class Clients(Subject):

    """ Clients class """

    def __init__(self, profile):

        """
        Initialization of Clients object.

        :param profile:     Profile Object
        :type  profile:     _profile
        """

        Subject.__init__(self, profile, Subject.CLIENT)
        self.api_base_url = self.profile.platform_url + "/api/v1/client"

    def get_clients(self, page_size=500, page_number=0):

        """
        Gets all clients associated with the API key.

        :param page_size:       Number of results to be returned on each page.
        :type  page_size:       int

        :param page_number:     The page number to be returned.
        :type  page_number:     int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        :raises PageSizeError:
        """

        url = self.api_base_url

        params = {
            "size": page_size,
            "page": page_number
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url, params=params)
        except (RequestFailed, StatusCodeError, MaxRetryError, PageSizeError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_client_info(self, client_id):

        """
        Gets the details for a specific client ID.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        url = self.api_base_url + "/" + str(client_id)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except (RequestFailed, StatusCodeError, MaxRetryError):
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_subjects(self, client_id=None):

        """
        List out all of the available subjects for a specific client.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    The JSON from the platform is returned.

        :raises RequestFailed:
        :raises StatusCodeError:
        :raises MaxRetryError:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url + "/" + str(client_id) + "/subject"

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
